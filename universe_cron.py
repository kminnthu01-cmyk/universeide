"""
Universe IDE - Cron Module

Scheduled tasks.
"""

from typing import Any, Callable, Dict, List
import time


# ============================================================================
# JOB
# ============================================================================

class CronJob:
    """Cron job"""
    
    def __init__(self, job_id: str, schedule: str, handler: Callable):
        self.job_id = job_id
        self.schedule = schedule
        self.handler = handler
        self.last_run = 0
        self.enabled = True
        
    def should_run(self, interval: int = 60) -> bool:
        if not self.enabled:
            return False
        now = time.time()
        if now - self.last_run >= interval:
            self.last_run = now
            return True
        return False
        
    def execute(self):
        if self.handler:
            return self.handler()


# ============================================================================
# CRON
# ============================================================================

class Cron:
    """Cron scheduler"""
    
    def __init__(self):
        self.jobs = {}
        
    def schedule(self, job: CronJob):
        self.jobs[job.job_id] = job
        
    def run_pending(self) -> List[Dict]:
        results = []
        for job in self.jobs.values():
            if job.should_run():
                try:
                    result = job.execute()
                    results.append({"job": job.job_id, "result": result})
                except:
                    pass
        return results


# Global
_cron = None

def get_cron() -> Cron:
    global _cron
    if _cron is None:
        _cron = Cron()
    return _cron


__all__ = ["CronJob", "Cron", "get_cron"]