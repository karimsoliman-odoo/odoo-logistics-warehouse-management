# Odoo Logistics & Warehouse Management

A portfolio-ready Odoo 20 custom module for logistics and warehouse operations.

This project demonstrates practical Odoo development across shipment tracking, warehouse storage billing, outbound workflows, access control, reporting, demo data, automated tests, and upgrade-friendly module design.

## Odoo Version
- Odoo 20.0
- Designed as an independent custom module
- No Odoo core modifications

## Implemented Features
- Automatic shipment reference sequence
- Customer assignment
- Company / multi-company support
- Entry and exit date tracking
- Quantity and CBM tracking
- Storage rate per day
- Automatic storage day calculation
- Automatic storage amount calculation
- Workflow: Draft -> Stored -> Outbound -> Done
- Cancel / Reset to Draft actions
- User and Manager security groups
- Multi-company record rule
- Search filters and Group By options
- List and Form views
- Printable Shipment Summary PDF report
- Demo data
- Automated tests for:
  - sequence generation
  - storage billing calculation
  - invalid date validation
  - negative storage rate validation
  - shipment workflow
- GitHub static checks for Python and XML files

## Business Use Case
The module is designed for logistics companies, warehouses, freight forwarders, and 3PL operations that need a lightweight shipment storage workflow.

Example process:

1. Register a shipment when cargo enters the warehouse.
2. Record quantity, CBM, entry date, and storage rate.
3. Odoo calculates storage duration and storage charges.
4. Move the shipment through operational states.
5. Record the exit date when cargo leaves.
6. Print a shipment summary report.

## Project Structure
```text
logistics_warehouse_management/
├── __init__.py
├── __manifest__.py
├── data/
│   └── logistics_sequence.xml
├── demo/
│   └── logistics_demo.xml
├── models/
│   ├── __init__.py
│   └── logistics_shipment.py
├── reports/
│   └── logistics_shipment_report.xml
├── security/
│   ├── ir.model.access.csv
│   └── logistics_security.xml
├── tests/
│   ├── __init__.py
│   └── test_logistics_shipment.py
└── views/
    ├── logistics_menus.xml
    └── logistics_shipment_views.xml
```

## Installation
1. Copy the `logistics_warehouse_management` folder into your custom addons path.
2. Add the custom addons path to the Odoo configuration if needed.
3. Restart Odoo.
4. Update the Apps list.
5. Search for **Logistics & Warehouse Management**.
6. Install the module.
7. Assign users to **Logistics User** or **Logistics Manager**.

## Security Model
- **Logistics User**
  - Read shipments
  - Create shipments
  - Update shipments
  - Cannot delete shipments

- **Logistics Manager**
  - Includes Logistics User permissions
  - Can delete shipments

- Users only see shipments for their allowed companies.

## Technical Highlights
- Odoo ORM
- `@api.model_create_multi`
- Computed stored fields
- Python constraints
- Monetary fields
- Sequence generation
- XML List / Form / Search views
- Window actions and menus
- Security groups and ACLs
- Multi-company record rules
- QWeb PDF reports
- Demo XML data
- TransactionCase automated testing
- GitHub-based development workflow

## Development Approach
The project follows an upgrade-friendly approach:
- all custom code stays inside a standalone addon;
- Odoo core is not modified;
- business logic is kept in models;
- security and UI definitions are separated;
- tests cover core calculations and workflow behavior.

This makes the module easier to maintain, migrate, and deploy across development, staging, Odoo.sh, or self-hosted environments.

## Portfolio Notice
This repository is an original demo/portfolio project. It contains no client production source code, credentials, private API keys, ZATCA certificates, or confidential business data.

## Author
**Karim Soliman**  
Odoo Functional / Implementation / Techno-Functional Consultant
