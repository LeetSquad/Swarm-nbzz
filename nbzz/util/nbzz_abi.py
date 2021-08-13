NBZZ_ABI =[
    {
        'constant': True,
        'inputs': [],
        'name': 'name',
        'outputs': [{'name': '', 'type': 'string'}],
        'payable': False,
        'stateMutability': 'view',
        'type': 'function'
    },
    {
        'constant': True,
        'inputs': [],
        'name': 'uBlockNumberd',
        'outputs': [{'name': '', 'type': 'uint256'}],
        'payable': False,
        'stateMutability': 'view',
        'type': 'function'
    },
    {
        'constant': True,
        'inputs': [],
        'name': 'baseStartTime',
        'outputs': [{'name': '', 'type': 'uint256'}],
        'payable': False,
        'stateMutability': 'view',
        'type': 'function'
    },
    {
        'constant': True,
        'inputs': [{'name': '_address', 'type': 'address'}],
        'name': 'addressPledge',
        'outputs': [{'name': '', 'type': 'uint256'}],
        'payable': False,
        'stateMutability': 'view',
        'type': 'function'
    },
    {
        'constant': False,
        'inputs': [],
        'name': 'killContract',
        'outputs': [{'name': '', 'type': 'bool'}],
        'payable': False,
        'stateMutability': 'nonpayable',
        'type': 'function'
    },
    {
        'constant': True,
        'inputs': [],
        'name': 'seeTrustNode',
        'outputs': [{'name': 'nodeaddress', 'type': 'address[]'}],
        'payable': False,
        'stateMutability': 'view',
        'type': 'function'
    },
    {
        'constant': True,
        'inputs': [],
        'name': 'lastBlockNumber',
        'outputs': [{'name': '', 'type': 'uint256'}],
        'payable': False,
        'stateMutability': 'view',
        'type': 'function'
    },
    {
        'constant': True,
        'inputs': [],
        'name': 'decimals',
        'outputs': [{'name': '', 'type': 'uint256'}],
        'payable': False,
        'stateMutability': 'view',
        'type': 'function'
    },
    {
        'constant': True,
        'inputs': [],
        'name': 'pledgeAmountAll',
        'outputs': [{'name': '', 'type': 'uint256'}],
        'payable': False,
        'stateMutability': 'view',
        'type': 'function'
    },
    {
        'constant': False,
        'inputs': [{'name': '_startTime', 'type': 'uint256'}],
        'name': 'setStartTime',
        'outputs': [{'name': 'success', 'type': 'bool'}],
        'payable': False,
        'stateMutability': 'nonpayable',
        'type': 'function'
    },
    {
        'constant': True,
        'inputs': [],
        'name': '_totalSupply',
        'outputs': [{'name': '', 'type': 'uint256'}],
        'payable': False,
        'stateMutability': 'view',
        'type': 'function'
    },
    {
        'constant': True,
        'inputs': [{'name': '_blcoknum', 'type': 'uint256'}],
        'name': 'uBlockd',
        'outputs': [
            {'name': '_blocknumber', 'type': 'uint256'},
            {'name': '_address', 'type': 'address[]'},
            {'name': '_amount', 'type': 'uint256[]'}
        ],
        'payable': False,
        'stateMutability': 'view',
        'type': 'function'
    },
    {
        'constant': True,
        'inputs': [],
        'name': 'founder',
        'outputs': [{'name': '', 'type': 'address'}],
        'payable': False,
        'stateMutability': 'view',
        'type': 'function'
    },
    {
        'constant': False,
        'inputs': [
            {'name': '_nodeaddress', 'type': 'address[]'},
            {'name': '_blocknumber', 'type': 'uint256'}
        ],
        'name': 'toDailyoutput',
        'outputs': [{'name': 'success', 'type': 'bool'}],
        'payable': False,
        'stateMutability': 'nonpayable',
        'type': 'function'
    },
    {
        'constant': False,
        'inputs': [{'name': '_address', 'type': 'address'}],
        'name': 'deltrustNode',
        'outputs': [{'name': 'success', 'type': 'bool'}],
        'payable': False,
        'stateMutability': 'nonpayable',
        'type': 'function'
    },
    {
        'constant': False,
        'inputs': [],
        'name': 'setStartCents',
        'outputs': [{'name': 'success', 'type': 'bool'}],
        'payable': False,
        'stateMutability': 'nonpayable',
        'type': 'function'
    },
    {
        'constant': True,
        'inputs': [{'name': '_address', 'type': 'address'}],
        'name': 'seeTrustNodeDetails',
        'outputs': [{'name': 'status', 'type': 'bool'}],
        'payable': False,
        'stateMutability': 'view',
        'type': 'function'
    },
    {
        'constant': True,
        'inputs': [],
        'name': 'airdropAll',
        'outputs': [{'name': '', 'type': 'uint256'}],
        'payable': False,
        'stateMutability': 'view',
        'type': 'function'
    },
    {
        'constant': True,
        'inputs': [],
        'name': 'pledgeAddressAlld',
        'outputs': [{'name': '', 'type': 'address[]'}],
        'payable': False,
        'stateMutability': 'view',
        'type': 'function'
    },
    {
        'constant': True,
        'inputs': [{'name': '_address', 'type': 'address'}],
        'name': 'balanceOf',
        'outputs': [{'name': 'balance', 'type': 'uint256'}],
        'payable': False,
        'stateMutability': 'view',
        'type': 'function'
    },
    {
        'constant': True,
        'inputs': [],
        'name': 'startCents',
        'outputs': [{'name': '', 'type': 'uint256'}],
        'payable': False,
        'stateMutability': 'view',
        'type': 'function'
    },
    {
        'constant': False,
        'inputs': [],
        'name': 'pledge',
        'outputs': [{'name': 'success', 'type': 'bool'}],
        'payable': False,
        'stateMutability': 'nonpayable',
        'type': 'function'
    },
    {
        'constant': True,
        'inputs': [],
        'name': 'symbol',
        'outputs': [{'name': '', 'type': 'string'}],
        'payable': False,
        'stateMutability': 'view',
        'type': 'function'
    },
    {
        'constant': False,
        'inputs': [
            {'name': '_to', 'type': 'address'},
            {'name': '_value', 'type': 'uint256'}
        ],
        'name': 'transfer',
        'outputs': [{'name': 'success', 'type': 'bool'}],
        'payable': False,
        'stateMutability': 'nonpayable',
        'type': 'function'
    },
    {
        'constant': True,
        'inputs': [{'name': '', 'type': 'uint256'}],
        'name': 'trustNodes',
        'outputs': [{'name': '', 'type': 'address'}],
        'payable': False,
        'stateMutability': 'view',
        'type': 'function'
    },
    {
        'constant': False,
        'inputs': [{'name': '_address', 'type': 'address'}],
        'name': 'setTrustNode',
        'outputs': [{'name': 'success', 'type': 'bool'}],
        'payable': False,
        'stateMutability': 'nonpayable',
        'type': 'function'
    },
    {
        'constant': True,
        'inputs': [],
        'name': 'distributedd',
        'outputs': [{'name': '', 'type': 'uint256'}],
        'payable': False,
        'stateMutability': 'view',
        'type': 'function'
    },
    {
        'constant': False,
        'inputs': [],
        'name': 'relief',
        'outputs': [{'name': 'success', 'type': 'bool'}],
        'payable': False,
        'stateMutability': 'nonpayable',
        'type': 'function'
    },
    {
        'constant': False,
        'inputs': [{'name': 'newFounder', 'type': 'address'}],
        'name': 'modifyOwnerFounder',
        'outputs': [{'name': 'founders', 'type': 'address'}],
        'payable': False,
        'stateMutability': 'nonpayable',
        'type': 'function'
    },
    {
        'constant': False,
        'inputs': [
            {'name': '_amount', 'type': 'uint256'},
            {'name': '_to', 'type': 'address'}
        ],
        'name': 'distribute',
        'outputs': [{'name': 'success', 'type': 'bool'}],
        'payable': False,
        'stateMutability': 'nonpayable',
        'type': 'function'
    },
    {
        'constant': True,
        'inputs': [{'name': '_address', 'type': 'address'}],
        'name': 'airdropd',
        'outputs': [{'name': '', 'type': 'uint256'}],
        'payable': False,
        'stateMutability': 'view',
        'type': 'function'
    },
    {
        'constant': True,
        'inputs': [],
        'name': 'startBlockHeight',
        'outputs': [{'name': '', 'type': 'uint256'}],
        'payable': False,
        'stateMutability': 'view',
        'type': 'function'
    },
    {'inputs': [], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'constructor'},
    {'payable': True, 'stateMutability': 'payable', 'type': 'fallback'},
    {
        'anonymous': False,
        'inputs': [{'indexed': True, 'name': 'sender', 'type': 'address'}],
        'name': 'AllocateFounderTokens',
        'type': 'event'
    },
    {
        'anonymous': False,
        'inputs': [
            {'indexed': True, 'name': '_from', 'type': 'address'},
            {'indexed': True, 'name': '_to', 'type': 'address'},
            {'indexed': False, 'name': '_value', 'type': 'uint256'}
        ],
        'name': 'Transfer',
        'type': 'event'
    },
    {
        'anonymous': False,
        'inputs': [
            {'indexed': True, 'name': '_owner', 'type': 'address'},
            {'indexed': True, 'name': '_spender', 'type': 'address'},
            {'indexed': False, 'name': '_value', 'type': 'uint256'}
        ],
        'name': 'Approval',
        'type': 'event'
    }
]