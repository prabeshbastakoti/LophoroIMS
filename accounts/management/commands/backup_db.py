import os
import subprocess
from datetime import datetime
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

BACKUP_DIR = settings.BASE_DIR / "backups"
PG_DUMP = os.getenv("PG_DUMP_PATH", "pg_dump")
KEEP_LAST = 10


class Command(BaseCommand):
    help = "Backup the PostgreSQL database to the backups/ directory"

    def add_arguments(self, parser):
        parser.add_argument(
            "--keep",
            type=int,
            default=KEEP_LAST,
            help=f"Number of recent backups to keep (default: {KEEP_LAST})",
        )

    def handle(self, *args, **options):
        BACKUP_DIR.mkdir(exist_ok=True)

        db = settings.DATABASES["default"]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = BACKUP_DIR / f"backup_{timestamp}.sql"

        env = os.environ.copy()
        env["PGPASSWORD"] = db.get("PASSWORD", "")

        cmd = [
            PG_DUMP,
            "--host", db.get("HOST", "localhost"),
            "--port", str(db.get("PORT", "5432")),
            "--username", db.get("USER", "postgres"),
            "--dbname", db.get("NAME", "lophoroims"),
            "--format", "plain",
            "--file", str(filename),
        ]

        self.stdout.write(f"Backing up to {filename} …")

        result = subprocess.run(cmd, env=env, capture_output=True, text=True)

        if result.returncode != 0:
            self.stderr.write(self.style.ERROR(f"Backup failed:\n{result.stderr}"))
            return

        size_kb = filename.stat().st_size // 1024
        self.stdout.write(self.style.SUCCESS(f"Backup saved ({size_kb} KB)"))

        self._cleanup(options["keep"])

    def _cleanup(self, keep):
        backups = sorted(BACKUP_DIR.glob("backup_*.sql"), reverse=True)
        old = backups[keep:]
        for f in old:
            f.unlink()
            self.stdout.write(f"Removed old backup: {f.name}")
        if old:
            self.stdout.write(f"Kept {keep} most recent backups.")
