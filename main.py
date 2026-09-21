import os
import sys
import logging
from config import get_settings
from cli import build_parser


def main():
    settings = get_settings()

    logging.basicConfig(
        level=settings["log_level"],
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler("service_manager.log", encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )

    parser = build_parser()
    args = parser.parse_args()

    if args.command == "client":
        if args.client_command == "add":
            # TODO: storage.add_client(args.name, args.phone, args.email)
            print(f"✅ Клієнта додано: {args.name} | {args.phone}")
        elif args.client_command == "list":
            # TODO: storage.list_clients()
            print("👥 Список клієнтів (підключіть storage)")
        elif args.client_command == "show":
            # TODO: storage.get_client(args.id)
            print(f"👤 Клієнт #{args.id} (підключіть storage)")

    elif args.command == "service":
        if args.service_command == "add":
            # TODO: storage.add_service(...)
            print(
                f"✅ Послугу додано: {args.name} — {args.price} {settings['currency']}")
        elif args.service_command == "list":
            print("🛠️  Список послуг (підключіть storage)")

    elif args.command == "order":
        if args.order_command == "create":
            # TODO: storage.create_order(args.client_id, args.service_id)
            print(
                f"✅ Замовлення створено: клієнт #{args.client_id}, послуга #{args.service_id}")
        elif args.order_command == "list":
            print("📋 Замовлення (підключіть storage)")
        elif args.order_command == "status":
            # TODO: storage.update_order_status(args.id, args.status)
            print(f"🔄 Статус замовлення #{args.id} → {args.status}")
        elif args.order_command == "delete":
            print(f"🗑️  Замовлення #{args.id} видалено")

    elif args.command == "report":
        print(f"📊 Звіт за період: {args.period} (підключіть storage)")

    elif args.command == "export":
        print(f"📤 Експорт у {args.format.upper()} (підключіть storage)")


if __name__ == "__main__":
    main()
