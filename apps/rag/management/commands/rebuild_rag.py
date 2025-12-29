from django.core.management.base import BaseCommand
from apps.clients.models import Client
from apps.rag.indexer import build_client_index


class Command(BaseCommand):
    help = "Rebuild FAISS RAG indexes"

    def add_arguments(self, parser):
        parser.add_argument(
            "--client-id",
            type=int,
            help="Rebuild index for a single client"
        )

    def handle(self, *args, **options):
        client_id = options.get("client_id")

        if client_id:
            path = build_client_index(client_id)
            self.stdout.write(self.style.SUCCESS(
                f"Index rebuilt for client {client_id}: {path}"
            ))
            return

        for client in Client.objects.all():
            path = build_client_index(client.id)
            if path:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Index rebuilt for client {client.id}"
                    )
                )
