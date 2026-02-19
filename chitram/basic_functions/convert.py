"""
basic_functions/convert.py

Author: Benevant Mathew
Date: 2025-12-16
"""
def metric_convert(val,current_unit,dest_unit):
    """
    Docstring for metric_convert

    :param val: Description
    :param current_unit: Description
    :param dest_unit: Description
    """
    if current_unit=='mm' and dest_unit=='inch':
        mm2inch=1/25.4
        return val*mm2inch
    elif current_unit=='cm' and dest_unit=='inch':
        cm2inch=1/2.54
        return val*cm2inch
    elif current_unit=='inch' and dest_unit=='mm':
        inch2mm=25.4
        return val*inch2mm
    elif current_unit=='inch' and dest_unit=='cm':
        inch2cm=2.54
        return val*inch2cm
