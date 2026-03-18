IT Consumable Management
========================
This module is designed for the "Base Developer Course" project and acts as an organic extension (addon) to the "IT Equipment Management" (bp_it_equipment) module.

Business Logic Context:
-----------------------
The company does not refill printer cartridges internally. Instead, it orders ready (refilled) cartridges and other IT peripherals (keyboards, mice, etc.) from suppliers as soon as the stock reaches minimum levels (Min-Max rule).

Key Features:
-------------
* Consumable catalog and category management.
* Tracking of available quantities and Min-Max inventory rules.
* Issue log to track consumables assigned to employees and specific equipment.
* Automated supplier request generation wizard for low-stock items.

Installation:
-------------
Standard Odoo module installation process. Requires 'base', 'mail', 'hr', and 'bp_it_equipment' modules.