"""
Universe IDE - Git Integration

Git workflow automation.
"""

import asyncio
import subprocess
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Callable, List, Optional


# ============================================================================
# GIT TYPES
# ============================================================================

class GitStatus(Enum):
    """Git status"""
    CLEAN = "clean"
    DIRTY = "dirty"
    AHEAD = "ahead"
    BEHIND = "behind"


@dataclass
class GitCommit:
    """Git commit"""
    hash: str
    message: str
    author: str
    timestamp: datetime
    files: List[str] = field(default_factory=list)


@dataclass
class GitBranch:
    """Git branch"""
    name: str
    is_current: bool = False
    is_remote: bool = False
    upstream: str = ""


@dataclass
class GitDiff:
    """Git diff"""
    file: str
    status: str  # M, A, D
    additions: int = 0
    deletions: int = 0
    patch: str = ""


# ============================================================================
# GIT MANAGER
# ============================================================================

class GitManager:
    """Git operations manager"""
    
    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path)
        
    def _run(self, *args) -> str:
        """Run git command"""
        cmd = ["git", *args]
        try:
            result = subprocess.run(
                cmd,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
            )
            return result.stdout.strip()
        except Exception as e:
            return str(e)
            
    # status
    def status(self) -> GitStatus:
        """Get repository status"""
        output = self._run("status", "--porcelain")
        if output.strip():
            return GitStatus.DIRTY
        return GitStatus.CLEAN
        
    def diff_status(self) -> List[GitDiff]:
        """Get diff status"""
        output = self._run("status", "--porcelain")
        diffs = []
        
        for line in output.split("\n"):
            if len(line) >= 3:
                status = line[:2].strip()
                file = line[3:]
                
                diffs.append(GitDiff(
                    file=file,
                    status=status,
                ))
                
        return diffs
        
    # Branches
    def branches(self) -> List[GitBranch]:
        """List branches"""
        output = self._run("branch", "-a")
        branches = []
        current = self._run("rev-parse", "--abbrev-ref", "HEAD")
        
        for line in output.split("\n"):
            if line:
                name = line.strip().replace("* ", "")
                branches.append(GitBranch(
                    name=name,
                    is_current=name == current,
                    is_remote="remotes" in line,
                ))
                
        return branches
        
    def create_branch(self, name: str, checkout: bool = True) -> bool:
        """Create branch"""
        self._run("branch", name)
        
        if checkout:
            self.checkout(name)
            
        return True
        
    def checkout(self, name: str) -> bool:
        """Checkout branch"""
        result = self._run("checkout", name)
        return result == ""
        
    def delete_branch(self, name: str, force: bool = False) -> bool:
        """Delete branch"""
        args = ["branch", "-d"] if force else ["branch", "-D"]
        args.append(name)
        
        result = self._run(*args)
        return result == ""
        
    # Commits
    def log(self, n: int = 10, stat: bool = True) -> List[GitCommit]:
        """Get commit history"""
        args = ["log", f"-n{n}"]
        if stat:
            args.append("--stat")
            
        output = self._run(*args)
        commits = []
        
        for chunk in output.split("\n---\n"):
            if chunk:
                lines = chunk.strip().split("\n")
                if lines:
                    # Parse commit
                    first_line = lines[0]
                    if "commit" in first_line:
                        hash = first_line.split()[1][:7]
                    else:
                        hash = "unknown"
                        
                    commits.append(GitCommit(
                        hash=hash,
                        message=first_line,
                        author="unknown",
                        timestamp=datetime.now(),
                    ))
                    
        return commits
        
    def commit(self, message: str, all: bool = True) -> str:
        """Create commit"""
        if all:
            self._run("add", "-A")
            
        result = self._run("commit", "-m", message)
        return result
        
    # Remote
    def push(self, remote: str = "origin", branch: str = None) -> str:
        """Push to remote"""
        args = ["push", remote]
        if branch:
            args.append(branch)
            
        return self._run(*args)
        
    def pull(self, remote: str = "origin", branch: str = None) -> str:
        """Pull from remote"""
        args = ["pull", remote]
        if branch:
            args.append(branch)
            
        return self._run(*args)
        
    def fetch(self, remote: str = "origin") -> str:
        """Fetch from remote"""
        return self._run("fetch", remote)
        
    # Diff
    def diff(self, target: str = None) -> str:
        """Get diff"""
        args = ["diff"]
        if target:
            args.append(target)
            
        return self._run(*args)
        
    def show(self, ref: str) -> str:
        """Show commit/file"""
        return self._run("show", ref)
        
    # Tags
    def tag(self, name: str, message: str = None) -> bool:
        """Create tag"""
        args = ["tag", name]
        if message:
            args.extend(["-m", message])
            
        result = self._run(*args)
        return result == ""
        
    def tags(self) -> List[str]:
        """List tags"""
        output = self._run("tag", "-l")
        return output.split("\n") if output else []
        
    # Stash
    def stash(self, message: str = None) -> str:
        """Stash changes"""
        args = ["stash", "push"]
        if message:
            args.extend(["-m", message])
            
        return self._run(*args)
        
    def stash_pop(self) -> str:
        """Pop stash"""
        return self._run("stash", "pop")


# ============================================================================
# GITHUB INTEGRATION
# ============================================================================

class GitHubIntegration:
    """GitHub-specific operations"""
    
    def __init__(self, token: str = None, owner: str = None, repo: str = None):
        self.token = token
        self.owner = owner
        self.repo = repo
        
    def create_pull_request(
        self, 
        title: str, 
        body: str, 
        head: str, 
        base: str = "main"
    ) -> dict:
        """Create pull request"""
        # Uses GitHub CLI or API
        # For now, return mock
        
        return {
            "number": 1,
            "title": title,
            "head": head,
            "base": base,
            "state": "open",
            "url": f"https://github.com/{self.owner}/{self.repo}/pull/1",
        }
        
    def list_pull_requests(self, state: str = "open") -> List[dict]:
        """List pull requests"""
        return [
            {
                "number": 1,
                "title": "Example PR",
                "state": state,
            }
        ]
        
    def merge_pull_request(self, number: int, method: str = "merge") -> dict:
        """Merge pull request"""
        return {
            "merged": True,
            "sha": "abc123",
            "message": "Merged PR #1",
        }
        
    def add_labels(self, issue: int, labels: List[str]) -> bool:
        """Add labels to issue/PR"""
        return True
        
    def assign_reviewers(self, number: int, reviewers: List[str]) -> bool:
        """Assign reviewers"""
        return True


# ============================================================================
# WORKFLOW AUTOMATION
# ============================================================================

@dataclass
class Workflow:
    """Git workflow definition"""
    name: str
    steps: List[dict]
    triggers: List[str] = field(default_factory=list)


class WorkflowAutomation:
    """Automate Git workflows"""
    
    WORKFLOWS = {
        "release": {
            "steps": [
                {"cmd": "git checkout main"},
                {"cmd": "git pull origin main"},
                {"cmd": "npm version patch"},
                {"cmd": "git push origin main"},
                {"cmd": "git tag v1.0.0"},
                {"cmd": "git push origin tag"},
            ]
        },
        "feature": {
            "steps": [
                {"cmd": "git checkout -b feature/xxx"},
                {"cmd": "git commit -m 'feat: add feature'"},
                {"cmd": "git push origin feature/xxx"},
            ]
        },
    }
    
    def __init__(self):
        self.git = GitManager()
        
    def run_workflow(self, name: str) -> dict:
        """Run workflow"""
        if name not in self.WORKFLOWS:
            return {"error": f"Unknown workflow: {name}"}
            
        workflow = self.WORKFLOWS[name]
        results = []
        
        for step in workflow["steps"]:
            try:
                cmd = step["cmd"]
                output = self.git._run(*cmd.split())
                results.append({"cmd": cmd, "success": True, "output": output})
            except Exception as e:
                results.append({"cmd": cmd, "success": False, "error": str(e)})
                
        return {"workflow": name, "results": results}
        
    def register_workflow(self, name: str, steps: List[dict]):
        """Register custom workflow"""
        self.WORKFLOWS[name] = {"steps": steps}


# Global
_git = None

def get_git(repo_path: str = ".") -> GitManager:
    """Get Git manager"""
    global _git
    if _git is None:
        _git = GitManager(repo_path)
    return _git


__all__ = [
    "GitStatus",
    "GitCommit",
    "GitBranch",
    "GitDiff",
    "GitManager",
    "GitHubIntegration",
    "Workflow",
    "WorkflowAutomation",
    "get_git",
]