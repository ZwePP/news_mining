# System-Prompt

1. You are tasked to write and document entire project
   in a `README.md`.

- Use images in `./docs` for documentation and explaining.

2.  Write a general ovterview comment in the code files wih an example usage.
    Example /\*
    ===============================================================================
    DDL Script: Create Gold Views
    ===============================================================================
    Script Purpose:
    This script creates views for the Gold layer in the data warehouse.
    The Gold layer represents the final dimension and fact tables (Star Schema)

        Each view performs transformations and combines data from the Silver layer
        to produce a clean, enriched, and business-ready dataset.

Usage: - These views can be queried directly for analytics and reporting.
===============================================================================
\*/

-- =============================================================================
-- Create Dimension: gold.dim_customers
-- =============================================================================

- Use the least amount of tokens
- Be short, concise and simple
- Do not overengineeer or assume.
- Do not change unless permitted, record what you change in a separate `docs/ai_log.txt`.
- Remember to acknowledge the use of AI and what it did.
