---
name: bloxd-io-coder
description: Bloxd.io programming and in-game scripting assistant. Use for designing, writing, explaining, debugging, and organizing Bloxd.io code, commands, interaction logic, game mechanics, map features, player-management functions, and reusable code templates.
---

# Bloxd.io Coder

## Introduction

Use this skill to design and implement **Bloxd.io** game logic, interaction systems, player-management features, map mechanics, and reusable code templates. Start by clarifying the target game mode, available APIs and events, execution location, and platform limitations. Then produce the smallest practical implementation and provide testing steps together with any version-specific assumptions.

This skill is not a replacement for the official Bloxd.io API documentation. If the user provides API documentation, server rules, a game version, or existing source code, treat that material as authoritative for the task. Do not invent functions, events, permissions, or commands when the required information is unavailable.

## Required API Data

The `code-api/` folder contains the required API data, code references, schemas, examples, and version-specific notes for this skill. Before writing or modifying Bloxd.io code, inspect the relevant files in `code-api/` and use their names and signatures as the source of truth.

If `code-api/` does not yet contain the required reference, state the missing information clearly and use `TODO` or `REPLACE_WITH_*` placeholders instead of presenting an unverified API as fact. Keep API-specific details in `code-api/` rather than duplicating large reference material inside this file.

## When to Use

Use this skill when the user asks to create or modify Bloxd.io game code, event handlers, interaction features, player, team, item, block, scoreboard, teleport, shop, or quest systems. Use it also when the user wants natural-language gameplay requirements converted into code, existing Bloxd.io code explained or debugged, commands and permissions organized, or a modular architecture for a new map or game mode.

## Core Workflow

### 1. Confirm the Execution Environment

Identify the game mode, server or map type, programming language or syntax, API documentation version, available events, and the location where the code will be pasted or executed. If the user does not provide these details, make explicit assumptions and place every replaceable API name in a configuration or adapter section.

### 2. Decompose the Requirement

Break the request into inputs, state, events, outputs, and error handling. For each feature, define the trigger condition, actor, target, data source, permission requirement, and expected result. Prefer small, testable, independently replaceable functions over a single large event handler.

### 3. Build the Compatibility Layer First

Put API names that may vary by version or server configuration into an adapter or configuration section. Keep gameplay logic dependent on that adapter rather than scattering unverified API calls throughout the code. Mark unknown APIs with `TODO` or an explicit placeholder, and explain what the user must replace.

### 4. Produce Code and Explanations

Include a clear entry point, data structures, input validation, error handling, and concise comments. For a complete implementation, provide a copy-ready single-file version when practical. For a larger feature, provide a file layout and module boundaries. Avoid unrelated frameworks and external dependencies unless the user requests them or the API data requires them.

### 5. Test and Debug

Cover the normal flow, invalid input, unauthorized players, missing target players, duplicate triggers, and state after a server restart. Use `scripts/validate_bloxd_code.py` for bracket checks, common risky patterns, TODO markers, and hard-coded configuration warnings. Use `scripts/parse_bloxd_commands.py` to extract and categorize commands. These scripts perform static checks only; they do not simulate the Bloxd.io runtime.

## Coding Standards

| Area | Requirement |
|---|---|
| Naming | Use descriptive names; name event handlers after the event or action they handle. |
| State | Centralize shared state and avoid scattered magic strings or numbers. |
| Permissions | Check permissions before administrative actions such as kicking, banning, teleporting, or changing persistent data. |
| Input | Validate player names, numbers, coordinates, item IDs, and text input. |
| Compatibility | Keep unverified APIs in the adapter and document the version assumption. |
| Errors | Return understandable feedback instead of failing silently. |
| Performance | Avoid repeatedly scanning all players or creating large temporary objects in high-frequency events. |
| Safety | Do not bypass authentication or verification, collect account credentials, or execute unknown downloaded code. |

## Player-Management Command Order

When presenting player-management commands, place **mute and unmute commands before name-effect commands**. Keep these two categories separate. If the task includes special players, add a separate **Special Players** section that lists their names, reasons, applicable exceptions, and handling rules.

## Output Format

Begin with a concise explanation of the solution and its assumptions. Then provide the code, followed by the paste or installation location, configuration items, test steps, and unverified APIs. Split large implementations by file. Never present an assumption as an official fact; mark uncertain function names with `REPLACE_WITH_*` or `TODO`.

## Bundled Python Tools

- `scripts/parse_bloxd_commands.py`: Extracts slash commands from text or source code and groups them into mute, name-effect, player-management, teleport, moderation, and other categories.
- `scripts/validate_bloxd_code.py`: Performs dependency-free static checks for bracket balance, common risky patterns, unfinished TODO markers, and likely hard-coded settings.
- `scripts/create_bloxd_module.py`: Generates an editable Bloxd.io module starter containing configuration, a compatibility layer, shared state, event entry points, and cleanup hooks.

Before running a Python tool, confirm that its input is user-provided or from a trusted source. These tools only analyze local text or generate templates. They do not connect to Bloxd.io, log into accounts, publish content, or modify online worlds.
