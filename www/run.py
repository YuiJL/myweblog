#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Jiayi Li'

from app import create_app

if __name__ == "__main__":
    app = create_app()
    app.run()