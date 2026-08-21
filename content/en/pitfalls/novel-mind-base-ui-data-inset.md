+++
title = 'The data-inset Styling Trap in base-ui'
date = 2026-07-18T04:47:00+08:00
draft = false
ShowToc = true
TocOpen = true
categories = ['pitfalls']
tags = ['base-ui', 'CSS', 'frontend']
projects = ['novel-mind']
description = 'The base-ui Menu never emits data-inset — the recipe layer sets it itself, so CSS selectors keyed on DOM data attributes come up empty.'
+++

The base-ui Menu component never emits a data-inset attribute, so the CSS selector finds nothing and the styling silently falls through.

<!--more-->

## Problem Description

The expectation was to control menu item indentation through the data-inset attribute. The CSS selector depends on [data-inset].

## Root Cause

The base-ui Menu does not emit data-inset. That attribute is set by the Radix DropdownMenuLabel/Item recipe layer itself. When you consume the base-ui Menu directly, data-inset simply does not exist.

## Solution

Confirm the component chain: base-ui → Radix recipe → custom data attributes. Styles must follow the conventions of the recipe layer.

## Prevention

Verify the component API surface before adopting base-ui; document each component's attribute contract.
