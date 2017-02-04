#!/bin/bash

pipdeptree -p Django > requirements.txt
pipdeptree -p djangorestframework >> requirements.txt
pipdeptree | grep -v '\s' >> requirements.txt
