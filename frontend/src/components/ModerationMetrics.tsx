'use client';

import React, { useCallback, useEffect, useState } from 'react';
import { apiService } from '@/lib/api';
import type { ModerationMetrics, ModerationStats } from '@/lib/api';
import { ErrorNote } from '@/components/studio/shared';

const scoreLabel = (score: number) =>
  score >= 90 ? 'Excellent' : score >= 70 ? 'Good' : score >= 50 ? 'Fair' : 'Poor';

const scoreColor = (score: number) =>
  score >= 90 ? 'text-genre-fantasy' : score >= 70 ? 'text-ink' : score >= 50 ? 'text-genre-thriller' : 'text-alert';

const humanize = (s: string) => s.replace(/_/g, ' ');

const SEVERITY: Record<string, string> = {
  high: 'bg-alert-tint text-alert',
  medium: 'bg-[#fbf1d9] text-[#7a560c]',
  low: 'bg-paper text-ink-soft',
};

const ModerationMetricsPanel: React.FC<{ className?: string }> = ({ className = '' }) => {
  const [metrics, setMetrics] = useState<ModerationMetrics | null>(null);
  const [stats, setStats] = useState<ModerationStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [period, setPeriod] = useState(30);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [m, s] = await Promise.all([
        apiService.getModerationMetrics(period),
        apiService.getModerationStats(period),
      ]);
      setMetrics(m);
      setStats(s);
    } catch (err: any) {
      setError(err?.response?.data?.detail || err?.message || 'Failed to load moderation metrics');
    } finally {
      setLoading(false);
    }
  }, [period]);

  useEffect(() => {
    load();
  }, [load]);

  const distribution = metrics ? Object.entries(metrics.safety_score_distribution) : [];
  const maxBucket = Math.max(1, ...distribution.map(([, c]) => Number(c)));
  const empty = metrics && metrics.total_content_moderated === 0;

  return (
    <section className={className} aria-busy={loading}>
      <div className="flex flex-wrap items-end justify-between gap-4 border-b border-rule pb-5">
        <div>
          <h1 className="font-display text-4xl font-bold leading-tight">Content safety</h1>
          <p className="mt-2 text-ink-soft">What the Content Moderator found in your content.</p>
        </div>
        <div>
          <label htmlFor="period" className="label text-sm">Period</label>
          <select id="period" value={period} onChange={(e) => setPeriod(Number(e.target.value))} className="field py-2">
            <option value={7}>Last 7 days</option>
            <option value={30}>Last 30 days</option>
            <option value={90}>Last 90 days</option>
          </select>
        </div>
      </div>

      {loading && (
        <div className="mt-8 animate-pulse space-y-4" aria-label="Loading">
          <div className="h-5 w-2/3 rounded bg-rule" />
          <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
            {[0, 1, 2, 3].map((i) => <div key={i} className="h-16 rounded bg-rule/70" />)}
          </div>
          <div className="h-40 rounded bg-rule/50" />
        </div>
      )}

      {!loading && error && (
        <div className="mt-8 max-w-xl">
          <ErrorNote message={error} onRetry={load} />
        </div>
      )}

      {!loading && !error && metrics && stats && (
        <>
          <p className="mt-6 max-w-3xl text-lg leading-relaxed">
            {empty ? (
              <>Nothing was moderated in the last {period} days.</>
            ) : (
              <>
                Over the last {period} days, {metrics.total_content_moderated} pieces of content were moderated, with an
                average safety score of {metrics.average_safety_score.toFixed(1)} ({scoreLabel(metrics.average_safety_score)}).
                {metrics.total_violations_found > 0 &&
                  ` ${metrics.total_violations_found} violations were found and ${metrics.total_unsafe_content} pieces were flagged as unsafe.`}
              </>
            )}
          </p>

          <dl className="tnum mt-8 grid grid-cols-2 divide-rule border-y border-rule md:grid-cols-4 md:divide-x">
            {[
              { label: 'Content moderated', value: metrics.total_content_moderated, cls: '' },
              { label: 'Violations found', value: metrics.total_violations_found, cls: metrics.total_violations_found ? 'text-alert' : '' },
              { label: 'Flagged unsafe', value: metrics.total_unsafe_content, cls: metrics.total_unsafe_content ? 'text-alert' : '' },
              {
                label: 'Average safety score',
                value: metrics.average_safety_score.toFixed(1),
                cls: empty ? '' : scoreColor(metrics.average_safety_score),
              },
            ].map((s) => (
              <div key={s.label} className="px-4 py-5 first:pl-0 md:first:pl-0">
                <dt className="text-sm text-ink-mute">{s.label}</dt>
                <dd className={`mt-1 font-display text-3xl font-bold ${s.cls}`}>{s.value}</dd>
              </div>
            ))}
          </dl>

          {!empty && (
            <div className="mt-12 grid gap-12 lg:grid-cols-2">
              <CountTable title="Violations by type" rows={Object.entries(metrics.violations_by_type)} />
              <CountTable title="Content by type" rows={Object.entries(metrics.content_by_type)} />

              <div className="lg:col-span-2">
                <h2 className="text-lg font-semibold">Safety score distribution</h2>
                <div className="mt-4 space-y-2.5">
                  {distribution.map(([range, count]) => (
                    <div key={range} className="grid grid-cols-[6rem_1fr_3rem] items-center gap-3 text-sm">
                      <span className="tnum text-ink-soft">{range}</span>
                      <div className="h-4 rounded-[2px] bg-paper">
                        <div
                          className="h-4 rounded-[2px] bg-ink"
                          style={{ width: `${(Number(count) / maxBucket) * 100}%` }}
                        />
                      </div>
                      <span className="tnum text-right font-semibold">{count}</span>
                    </div>
                  ))}
                </div>
              </div>

              {stats.violation_breakdown.length > 0 && (
                <div className="lg:col-span-2">
                  <h2 className="text-lg font-semibold">Violation breakdown</h2>
                  <table className="tnum mt-4 w-full text-left text-sm">
                    <thead>
                      <tr className="border-b border-ink/20 text-ink-mute">
                        <th className="py-2 font-semibold">Type</th>
                        <th className="py-2 text-right font-semibold">Violations</th>
                        <th className="py-2 text-right font-semibold">Share of content</th>
                        <th className="py-2 pl-6 font-semibold">Severity</th>
                      </tr>
                    </thead>
                    <tbody>
                      {stats.violation_breakdown.map((v, i) => (
                        <tr key={i} className="border-b border-rule">
                          <td className="py-3 capitalize">{humanize(v.violation_type)}</td>
                          <td className="py-3 text-right">{v.count}</td>
                          <td className="py-3 text-right">{v.percentage}%</td>
                          <td className="py-3 pl-6">
                            <span className={`rounded-[2px] px-2 py-0.5 text-xs font-semibold capitalize ${SEVERITY[v.severity] || SEVERITY.low}`}>
                              {v.severity}
                            </span>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          )}
        </>
      )}
    </section>
  );
};

function CountTable({ title, rows }: { title: string; rows: [string, unknown][] }) {
  return (
    <div>
      <h2 className="text-lg font-semibold">{title}</h2>
      {rows.length === 0 ? (
        <p className="mt-4 text-ink-mute">None in this period.</p>
      ) : (
        <table className="tnum mt-4 w-full text-sm">
          <tbody>
            {rows.map(([k, v]) => (
              <tr key={k} className="border-b border-rule">
                <td className="py-2.5 capitalize text-ink-soft">{humanize(k)}</td>
                <td className="py-2.5 text-right font-semibold">{String(v)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default ModerationMetricsPanel;
