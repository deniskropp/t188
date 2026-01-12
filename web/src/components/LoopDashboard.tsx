import React, { useEffect, useState } from 'react';
import { loopApi } from '../lib/api';
import { motion } from 'framer-motion';
import { Activity, Target, Zap, Heart, Layers, Loader2 } from 'lucide-react';

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
        <div className="flex flex-col gap-5 p-5 bg-white/[0.03] backdrop-blur-2xl border border-white/10 rounded-3xl text-white shadow-xl">
            <header className="flex items-center justify-between border-b border-white/5 pb-3">
                <div>
                    <h2 className="text-sm font-black tracking-tighter uppercase italic flex items-center gap-2">
                        <Activity className="text-meta-accent" size={14} />
                        Engine Stats
                    </h2>
                </div>
                <div className="flex flex-col items-end">
                    <div className="text-[9px] text-zinc-500 font-mono uppercase tracking-tighter">
                        EI: {((status.engagement_index || 0) * 100).toFixed(1)}
                    </div>
                </div>
            </header>

            {/* Engagement Gauge */}
            <div className="relative h-16 flex flex-col items-center justify-center bg-gradient-to-b from-white/[0.02] to-transparent rounded-xl border border-white/5">
                <div className="text-2xl font-black italic tracking-tighter text-white">
                    {((status.engagement_index || 0) * 100).toFixed(0)}
                    <span className="text-[10px] text-zinc-500 not-italic ml-1">EI</span>
                </div>
            </div>

            {/* Metrics Grid */}
            <div className="grid grid-cols-2 gap-2">
                <div className="bg-white/[0.02] p-2 rounded-lg border border-white/5">
                    <div className="flex items-center gap-1.5 mb-1">
                        <Zap className="text-yellow-400" size={10} />
                        <span className="text-[8px] font-bold text-zinc-500 uppercase tracking-widest">Dopamin</span>
                    </div>
                    <div className="text-sm font-black italic">{((status.dopamine_density || 0) * 100).toFixed(0)}%</div>
                </div>

                <div className="bg-white/[0.02] p-2 rounded-lg border border-white/5">
                    <div className="flex items-center gap-1.5 mb-1">
                        <Heart className="text-rose-400" size={10} />
                        <span className="text-[8px] font-bold text-zinc-500 uppercase tracking-widest">Bond</span>
                    </div>
                    <div className="text-sm font-black italic">{((status.oxytocin_level || 0) * 100).toFixed(0)}%</div>
                </div>
            </div>

            {/* Placebo Pipes */}
            {status.current_pipes && status.current_pipes.length > 0 && (
                <div className="space-y-1.5">
                    <div className="flex items-center gap-1.5 text-[8px] font-bold text-zinc-500 uppercase tracking-widest px-1">
                        <Layers size={10} />
                        Transport
                    </div>
                    <div className="space-y-1">
                        {status.current_pipes.map((pipe: string, i: number) => (
                            <div key={i} className="flex items-center gap-2 px-2 py-1.5 bg-white/[0.01] border border-white/5 rounded-md">
                                <motion.div 
                                    className="w-1 h-1 bg-meta-accent rounded-full"
                                    animate={{ opacity: [0, 1, 0] }}
                                    transition={{ duration: 1, repeat: Infinity, delay: i * 0.3 }}
                                />
                                <span className="text-[10px] font-mono text-zinc-400 tracking-tighter truncate">{pipe}</span>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* Active Quests */}
            {status.active_quests && status.active_quests.length > 0 && (
                <div className="flex flex-col gap-1.5">
                    <h3 className="text-[8px] font-bold text-zinc-500 uppercase tracking-widest px-1 flex items-center gap-1.5">
                        <Target size={10} />
                        Quests
                    </h3>
                    <div className="space-y-1.5">
                        {status.active_quests.map((quest: any) => (
                            <div key={quest.id} className="bg-white/[0.02] p-2 rounded-lg border border-white/5">
                                <div className="flex justify-between items-start mb-1">
                                    <div className="text-[10px] font-bold text-zinc-300">{quest.title}</div>
                                    {quest.status === 'completed' && (
                                        <button 
                                            onClick={() => loopApi.claimBadge(quest.id).then(fetchStatus)}
                                            className="text-[8px] px-1.5 py-0.5 bg-meta-accent/20 text-meta-accent rounded border border-meta-accent/30 font-bold"
                                        >
                                            CLAIM
                                        </button>
                                    )}
                                </div>
                                <div className="w-full bg-white/5 h-0.5 rounded-full overflow-hidden">
                                    <motion.div 
                                        className="bg-meta-accent h-full"
                                        animate={{ width: `${(quest.progress || 0) * 100}%` }}
                                    />
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
};
