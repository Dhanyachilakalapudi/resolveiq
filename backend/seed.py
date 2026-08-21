from app.database import Base, SessionLocal, engine
from app.models import ExceptionRecord


def seed_database():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    existing = db.query(ExceptionRecord).count()

    if existing > 0:
        print(f"Database already contains {existing} records.")
        db.close()
        return

    exceptions = [
        ExceptionRecord(
            exception_id="EXC-1001",
            invoice_id="INV-1042",
            vendor="Acme Supplies",
            exception_type="PRICE_MISMATCH",
            description="Invoice unit price exceeds the approved purchase order price.",
            expected_value=100.00,
            actual_value=125.00,
            difference=25.00,
            severity="HIGH",
            status="PENDING"
        ),

        ExceptionRecord(
            exception_id="EXC-1002",
            invoice_id="INV-1047",
            vendor="Global Office Ltd",
            exception_type="QUANTITY_MISMATCH",
            description="Invoice quantity is greater than the purchase order quantity.",
            expected_value=50.00,
            actual_value=65.00,
            difference=15.00,
            severity="HIGH",
            status="PENDING"
        ),

        ExceptionRecord(
            exception_id="EXC-1003",
            invoice_id="INV-1051",
            vendor="TechSource Inc",
            exception_type="DUPLICATE_INVOICE",
            description="A matching invoice from the same vendor already exists.",
            expected_value=1.00,
            actual_value=2.00,
            difference=1.00,
            severity="MEDIUM",
            status="PENDING"
        ),

        ExceptionRecord(
            exception_id="EXC-1004",
            invoice_id="INV-1058",
            vendor="Metro Services",
            exception_type="TAX_ANOMALY",
            description="Calculated tax differs from the expected tax amount.",
            expected_value=180.00,
            actual_value=216.00,
            difference=36.00,
            severity="MEDIUM",
            status="PENDING"
        ),

        ExceptionRecord(
            exception_id="EXC-1005",
            invoice_id="INV-1063",
            vendor="NorthStar Logistics",
            exception_type="MISSING_PO",
            description="Invoice cannot be matched to an existing purchase order.",
            expected_value=None,
            actual_value=4200.00,
            difference=None,
            severity="HIGH",
            status="PENDING"
        ),

        ExceptionRecord(
            exception_id="EXC-1006",
            invoice_id="INV-1069",
            vendor="Acme Supplies",
            exception_type="PRICE_MISMATCH",
            description="Invoice price is slightly above the configured tolerance.",
            expected_value=200.00,
            actual_value=210.00,
            difference=10.00,
            severity="LOW",
            status="PENDING"
        ),

        ExceptionRecord(
            exception_id="EXC-1007",
            invoice_id="INV-1074",
            vendor="BrightOffice",
            exception_type="QUANTITY_MISMATCH",
            description="Received quantity differs from the invoiced quantity.",
            expected_value=100.00,
            actual_value=102.00,
            difference=2.00,
            severity="LOW",
            status="PENDING"
        ),

        ExceptionRecord(
            exception_id="EXC-1008",
            invoice_id="INV-1080",
            vendor="CloudParts",
            exception_type="DUPLICATE_INVOICE",
            description="Invoice number and amount closely match a previous transaction.",
            expected_value=1.00,
            actual_value=1.00,
            difference=0.00,
            severity="MEDIUM",
            status="PENDING"
        )
    ]

    db.add_all(exceptions)
    db.commit()

    print(f"Successfully inserted {len(exceptions)} exception records.")

    db.close()


if __name__ == "__main__":
    seed_database()
