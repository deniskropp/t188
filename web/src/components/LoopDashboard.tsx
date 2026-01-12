import React, { useEffect, useState } from 'react';
import { loopApi } from '../lib/api';
import { motion } from 'framer-motion';
import { Activity, Zap, Heart, Layers, Loader2 } from 'lucide-react';

export const LoopDashboard: React.FC = () => {
    const [status, setStatus] = useState<any>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const fetchStatus = async () => {
        try {
            const data = await loopApi.getStatus();
            if (data) {
                setStatus(data);
                setError(null);
            }
        } catch (err: any) {
            console.error('Failed to fetch loop status', err);
            setError(err.message || 'Connection Error');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchStatus();
        const interval = setInterval(fetchStatus, 3000);
        return () => clearInterval(interval);
    }, []);

    if (loading && !status) return (
        <div className="flex flex-col items-center justify-center p-8 bg-white/[0.03] border border-white/5 rounded-3xl min-h-[100px]">
            <Loader2 className="animate-spin text-meta-accent mb-2" size={20} />
            <span className="text-[10px] uppercase font-bold text-zinc-600 tracking-widest">Initialising...</span>
        </div>
    );

    if (error && !status) return (
        <div className="p-4 bg-red-500/10 border border-red-500/20 rounded-2xl text-[10px] text-red-400 font-bold uppercase tracking-widest">
            {error}
        </div>
    );

    if (!status) return null;


    return (
        <div className="flex flex-col gap-4 p-4 bg-meta-surface border border-meta-border rounded-xl text-meta-main shadow-2xl transition-colors duration-300">
            <header className="flex items-center justify-between border-b border-meta-border pb-3">
                <div className="flex items-center gap-2">
                    <Activity className="text-meta-accent" size={14} />
                    <h2 className="text-[10px] font-black tracking-[0.2em] uppercase italic text-meta-muted">
                        Engine Stats
                    </h2>
                </div>
                <div className="text-[9px] text-meta-muted font-bold uppercase tracking-tighter">
                    EI: {((status.engagement_index || 0) * 100).toFixed(1)}
                </div>
            </header>

            {/* Engagement Gauge */}
            <div className="bg-meta-surface-hover p-4 rounded-lg border border-meta-border flex flex-col items-center justify-center relative overflow-hidden group">
                <div className="absolute inset-0 bg-gradient-to-br from-meta-accent/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
                <div className="text-3xl font-black italic tracking-tighter text-meta-main relative z-10">
                    {((status.engagement_index || 0) * 100).toFixed(0)}
                    <span className="text-[10px] text-meta-muted not-italic ml-1 uppercase font-bold tracking-[0.1em]">EI</span>
                </div>
                <div className="w-10 h-1 bg-meta-surface mt-2 rounded-full overflow-hidden">
                    <motion.div 
                        className="bg-meta-accent h-full"
                        animate={{ width: `${(status.engagement_index || 0) * 100}%` }}
                    />
                </div>
            </div>

            {/* Metrics Grid */}
            <div className="grid grid-cols-2 gap-2">
                <div className="bg-meta-surface-hover p-3 rounded-lg border border-meta-border hover:border-yellow-500/20 transition-all">
                    <div className="flex items-center gap-1.5 mb-1">
                        <Zap className="text-yellow-400" size={10} />
                        <span className="text-[8px] font-black text-meta-muted uppercase tracking-widest">Dopamin</span>
                    </div>
                    <div className="text-lg font-black italic">{((status.dopamine_density || 0) * 100).toFixed(0)}%</div>
                </div>

                <div className="bg-meta-surface-hover p-3 rounded-lg border border-meta-border hover:border-rose-500/20 transition-all">
                    <div className="flex items-center gap-1.5 mb-1">
                        <Heart className="text-rose-400" size={10} />
                        <span className="text-[8px] font-black text-meta-muted uppercase tracking-widest">Bond</span>
                    </div>
                    <div className="text-lg font-black italic">{((status.oxytocin_level || 0) * 100).toFixed(0)}%</div>
                </div>
            </div>

            {/* Placebo Pipes */}
            {status.current_pipes && status.current_pipes.length > 0 && (
                <div className="space-y-3">
                    <div className="flex items-center gap-2 text-[9px] font-black text-meta-muted uppercase tracking-[0.2em] px-1">
                        <Layers size={14} />
                        Transport
                    </div>
                    <div className="space-y-2">
                        {status.current_pipes.map((pipe: string, i: number) => (
                            <div key={i} className="flex items-center gap-3 px-3 py-2 bg-meta-surface-hover border border-meta-border rounded-lg group hover:bg-meta-surface transition-all">
                                <motion.div 
                                    className="w-1.5 h-1.5 bg-meta-accent rounded-full shadow-[0_0_8px_rgba(139,92,246,0.5)]"
                                    animate={{ 
                                        opacity: [0.3, 1, 0.3],
                                        scale: [0.8, 1.2, 0.8]
                                    }}
                                    transition={{ duration: 2, repeat: Infinity, delay: i * 0.4 }}
                                />
                                <span className="text-[10px] font-bold text-meta-muted tracking-tight truncate group-hover:text-meta-main">{pipe}</span>
                            </div>
                        ))}
                    </div>
                </div>
            )}
            {/* Active Quests (Re-integrated) */}
            <section className="pt-2 border-t border-meta-border">
                <div className="flex items-center gap-2 mb-4 px-2">
                    <div className="p-1 px-2 bg-purple-500/10 rounded-md border border-purple-500/20">
                        <span className="text-[8px] font-black text-purple-400 uppercase tracking-widest leading-none">Objective</span>
                    </div>
                    <h2 className="text-[10px] font-black tracking-[0.2em] uppercase text-meta-muted italic">Neural Quests</h2>
                </div>
                <div className="grid grid-cols-1 gap-2">
                    {status.active_quests.map((q: any) => (
                        <div key={q.id} className="group flex items-center justify-between p-4 bg-meta-surface-hover border border-meta-border rounded-lg hover:border-purple-500/20 transition-all">
                            <div className="flex-1 min-w-0">
                                <div className="text-[10px] font-black text-meta-main uppercase tracking-tighter mb-1">{q.title}</div>
                                <div className="text-[9px] text-meta-muted font-medium truncate">{q.description}</div>
                            </div>
                            <div className="ml-4 flex items-center gap-3">
                                <div className="w-24 h-1 bg-meta-surface rounded-full overflow-hidden">
                                     <motion.div 
                                        initial={{ width: 0 }}
                                        animate={{ width: `${q.progress * 100}%` }}
                                        className="h-full bg-purple-500/50" 
                                     />
                                </div>
                                <span className="text-[10px] font-mono text-meta-muted">{Math.round(q.progress * 100)}%</span>
                            </div>
                        </div>
                    ))}
                </div>
            </section>
        </div>
    );
};
