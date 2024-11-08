# policies.py
TOC_REFUND_POLICIES = {
    'EM': [
        (15, 29, 0.25),
        (30, 59, 0.5),
        (60, 119, 1.0),
        (120, float('inf'), 1.0, 'return')
    ],
    'GW': [
        (15, 29, 0.25),
        (30, 59, 0.5),
        (60, 119, 1.0),
        (120, float('inf'), 1.0, 'return')
    ],
    'SE': [
        (15, 29, 0.25),
        (30, 59, 0.5),
        (60, 119, 1.0),
        (120, float('inf'), 1.0, 'return')
    ],
    'SW': [
        (15, 29, 0.25),
        (30, 59, 0.5),
        (60, float('inf'), 1.0)
    ],
    'CH': [
        (15, 29, 0.25),
        (30, 59, 0.5),
        (60, float('inf'), 1.0)
    ],
    'XC': [
        (30, 59, 0.5),
        (60, float('inf'), 1.0)
    ]
}

TOC_NAMES = {
    'EM': 'East Midlands Railway',
    'SW': 'South Western Railway',
    'GW': 'Great Western Railway',
    'CH': 'Chiltern Railways',
    'XC': 'CrossCountry',
    'SE': 'Southeastern',
    # Add other TOC codes if necessary
}