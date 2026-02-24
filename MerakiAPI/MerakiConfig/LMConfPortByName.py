

PORT_PROFILES_STORE = {
    "firewall_lan": {
        "priority": 100,
        "pattern": r"firewall.*lan|lan.*firewall",
        "payload": {
            "tags": [],
            "enabled": False,
            "poeEnabled": False,
            "type": "trunk",
            "vlan": 1,
            "voiceVlan": None,
            "allowedVlans": "301-304,306,307,311,312,320,321,323-325",
            "activeVlans": "301-304,306-307,311-312,320-321,323-325",
            "isolationEnabled": False,
            "rstpEnabled": False,
            "stpGuard": "disabled",
            "linkNegotiation": "Auto negotiate",
            "portScheduleId": None,
            "schedule": None,
            "udld": "Alert only",
            "accessPolicyType": "Open",
            "daiTrusted": False,
            "profile": {
                "enabled": False,
                "id": "",
                "iname": None
            },
            "module": {
                "model": None    
            },
            "mirror": {
                "mode": "Not mirroring traffic"
            }
        }
    },
    "ap|ponteradio--Trunk-vlan307": {
        "priority": 90,
        "pattern": r"ap\d+|.*uplink_bridge.*",
        "payload": {
            "tags": [],
            "enabled": True,
            "poeEnabled": True,
            "type": "trunk",
            "vlan": 307,
            "voiceVlan": None,
            "allowedVlans": "304,306-307,320,323",
            "activeVlans": "304,306-307,320,323",
            "isolationEnabled": False,
            "rstpEnabled": True,
            "stpGuard": "disabled",
            "linkNegotiation": "Auto negotiate",
            "portScheduleId": None,
            "schedule": None,
            "udld": "Alert only",
            "accessPolicyType": "Open",
            "daiTrusted": False,
            "profile": {
                "enabled": False,
                "id": "",
                "iname": None
            },
            "module": {
                "model": None
            },
            "mirror": {
                "mode": "Not mirroring traffic"
            }
         }
    },
    "aplabel-vlan307": {
        "priority": 50,
        "pattern": r"\b(aplabel/)\b",
        "payload": {
            "tags": [],
            "enabled": True,
            "poeEnabled": True,
            "type": "access",
            "vlan": 307,
            "voiceVlan": None,
            "allowedVlans": "all",
            "activeVlans": "1-4094",
            "isolationEnabled": False,
            "rstpEnabled": True,
            "stpGuard": "disabled",
            "linkNegotiation": "Auto negotiate",
            "portScheduleId": None,
            "schedule": None,
            "udld": "Alert only",
            "accessPolicyType": "Open",
            "daiTrusted": False,
            "profile": {
                "enabled": False,
                "id": "",
                "iname": None
            },
            "module": {
                "model": None
            },
            "mirror": {
                "mode": "Not mirroring traffic"
            }
         }
    },
    "cassa-vlan301": {
        "priority": 50,
        "pattern": r"\b(cassa/)\b",
        "payload": {
            "tags": [],
            "enabled": True,
            "poeEnabled": False,
            "type": "access",
            "vlan": 301,
            "voiceVlan": None,
            "allowedVlans": "all",
            "activeVlans": "1-4094",
            "isolationEnabled": False,
            "rstpEnabled": True,
            "stpGuard": "disabled",
            "linkNegotiation": "Auto negotiate",
            "portScheduleId": None,
            "schedule": None,
            "udld": "Alert only",
            "accessPolicyType": "Open",
            "daiTrusted": False,
            "profile": {
                "enabled": False,
                "id": "",
                "iname": None
            },
            "module": {
                "model": None
            },
            "mirror": {
                "mode": "Not mirroring traffic"
            }
         }
    },
    "cash-new-vlan321": {
        "priority": 50,
        "pattern": r"\b(cash-new/)\b",
        "payload": {
            "tags": [],
            "enabled": True,
            "poeEnabled": False,
            "type": "access",
            "vlan": 321,
            "voiceVlan": None,
            "allowedVlans": "all",
            "activeVlans": "1-4094",
            "isolationEnabled": False,
            "rstpEnabled": True,
            "stpGuard": "disabled",
            "linkNegotiation": "Auto negotiate",
            "portScheduleId": None,
            "schedule": None,
            "udld": "Alert only",
            "accessPolicyType": "Open",
            "daiTrusted": False,
            "profile": {
                "enabled": False,
                "id": "",
                "iname": None
            },
            "module": {
                "model": None
            },
            "mirror": {
                "mode": "Not mirroring traffic"
            }
         }
    },
    "strongbox-vlan312": {
        "priority": 50,
        "pattern": r"\b(strongbox/)\b",
        "payload": {
            "tags": [],
            "enabled": True,
            "poeEnabled": False,
            "type": "access",
            "vlan": 312,
            "voiceVlan": None,
            "allowedVlans": "all",
            "activeVlans": "1-4094",
            "isolationEnabled": False,
            "rstpEnabled": True,
            "stpGuard": "disabled",
            "linkNegotiation": "Auto negotiate",
            "portScheduleId": None,
            "schedule": None,
            "udld": "Alert only",
            "accessPolicyType": "Open",
            "daiTrusted": False,
            "profile": {
                "enabled": False,
                "id": "",
                "iname": None
            },
            "module": {
                "model": None
            },
            "mirror": {
                "mode": "Not mirroring traffic"
            }
         }
    },
    "client-vlan304": {
        "priority": 60,
        "pattern": r"\b(client/|monitor/)\b",
        "payload": {
            "tags": [],
            "enabled": True,
            "poeEnabled": False,
            "type": "access",
            "vlan": 304,
            "voiceVlan": None,
            "allowedVlans": "all",
            "activeVlans": "1-4094",
            "isolationEnabled": False,
            "rstpEnabled": True,
            "stpGuard": "disabled",
            "linkNegotiation": "Auto negotiate",
            "portScheduleId": None,
            "schedule": None,
            "udld": "Alert only",
            "accessPolicyType": "Open",
            "daiTrusted": False,
            "profile": {
                "enabled": False,
                "id": "",
                "iname": None
            },
            "module": {
                "model": None
            },
            "mirror": {
                "mode": "Not mirroring traffic"
            }
         }
    },
    "bms-vlan325": {
        "priority": 60,
        "pattern": r"\b(bms/)\b",
        "payload": {
            "tags": [],
            "enabled": True,
            "poeEnabled": False,
            "type": "access",
            "vlan": 325,
            "voiceVlan": None,
            "allowedVlans": "all",
            "activeVlans": "1-4094",
            "isolationEnabled": False,
            "rstpEnabled": True,
            "stpGuard": "disabled",
            "linkNegotiation": "Auto negotiate",
            "portScheduleId": None,
            "schedule": None,
            "udld": "Alert only",
            "accessPolicyType": "Open",
            "daiTrusted": False,
            "profile": {
                "enabled": False,
                "id": "",
                "iname": None
            },
            "module": {
                "model": None
            },
            "mirror": {
                "mode": "Not mirroring traffic"
            }
         }
    },
    "fornitori-vlan302": {
        "priority": 60,
        "pattern": r"\b(fornitori/|pagodil)\b",
        "payload": {
            "tags": [],
            "enabled": True,
            "poeEnabled": False,
            "type": "access",
            "vlan": 302,
            "voiceVlan": None,
            "allowedVlans": "all",
            "activeVlans": "1-4094",
            "isolationEnabled": False,
            "rstpEnabled": True,
            "stpGuard": "disabled",
            "linkNegotiation": "Auto negotiate",
            "portScheduleId": None,
            "schedule": None,
            "udld": "Alert only",
            "accessPolicyType": "Open",
            "daiTrusted": False,
            "profile": {
                "enabled": False,
                "id": "",
                "iname": None
            },
            "module": {
                "model": None
            },
            "mirror": {
                "mode": "Not mirroring traffic"
            }
         }
    },
    "printer-vlan306": {
        "priority": 60,
        "pattern": r"\b(printer/)\b",
        "payload": {
            "tags": [],
            "enabled": True,
            "poeEnabled": False,
            "type": "access",
            "vlan": 306,
            "voiceVlan": None,
            "allowedVlans": "all",
            "activeVlans": "1-4094",
            "isolationEnabled": False,
            "rstpEnabled": True,
            "stpGuard": "disabled",
            "linkNegotiation": "Auto negotiate",
            "portScheduleId": None,
            "schedule": None,
            "udld": "Alert only",
            "accessPolicyType": "Open",
            "daiTrusted": False,
            "profile": {
                "enabled": False,
                "id": "",
                "iname": None
            },
            "module": {
                "model": None
            },
            "mirror": {
                "mode": "Not mirroring traffic"
            }
         }
    },
    "tvcc-vlan311": {
        "priority": 60,
        "pattern": r"\b(tvcc/|facility/)\b",
        "payload": {
            "tags": [],
            "enabled": True,
            "poeEnabled": True,
            "type": "access",
            "vlan": 311,
            "voiceVlan": None,
            "allowedVlans": "all",
            "activeVlans": "1-4094",
            "isolationEnabled": False,
            "rstpEnabled": True,
            "stpGuard": "disabled",
            "linkNegotiation": "Auto negotiate",
            "portScheduleId": None,
            "schedule": None,
            "udld": "Alert only",
            "accessPolicyType": "Open",
            "daiTrusted": False,
            "profile": {
                "enabled": False,
                "id": "",
                "iname": None
            },
            "module": {
                "model": None
            },
            "mirror": {
                "mode": "Not mirroring traffic"
            }
         }
    },
    "disable-by-user": {
        "priority": 40,
        "pattern": r"^\*{3}",
        "payload": {
            "tags": [],
            "enabled": False,
            "poeEnabled": False,
            "type": "access",
            "vlan": 1,
            "voiceVlan": None,
            "allowedVlans": "all",
            "activeVlans": "1,101-103,301-304,306-307,311-312,320-321,323-325",
            "isolationEnabled": False,
            "rstpEnabled": True,
            "stpGuard": "disabled",
            "linkNegotiation": "Auto negotiate",
            "portScheduleId": None,
            "schedule": None,
            "udld": "Alert only",
            "accessPolicyType": "Open",
            "daiTrusted": False,
            "profile": {
                "enabled": False,
                "id": "",
                "iname": None
            },
            "module": {
                "model": None
            },
            "mirror": {
                "mode": "Not mirroring traffic"
            }
         }
    },
    "shut": {
        "priority": 40,
        "payload": {
            "tags": [],
            "enabled": False,
            "poeEnabled": False,
            "type": "access",
            "vlan": 1,
            "voiceVlan": None,
            "allowedVlans": "all",
            "activeVlans": "1,101-103,301-304,306-307,311-312,320-321,323-325",
            "isolationEnabled": False,
            "rstpEnabled": True,
            "stpGuard": "disabled",
            "linkNegotiation": "Auto negotiate",
            "portScheduleId": None,
            "schedule": None,
            "udld": "Alert only",
            "accessPolicyType": "Open",
            "daiTrusted": False,
            "profile": {
                "enabled": False,
                "id": "",
                "iname": None
            },
            "module": {
                "model": None
            },
            "mirror": {
                "mode": "Not mirroring traffic"
            }
         }
    },
    "wan-3-fex-vlan103": {
        "priority": 60,
        "pattern": r"\b(fex|rtr-wan-3)\b",
        "payload": {
            "tags": [],
            "enabled": True,
            "poeEnabled": True,
            "type": "access",
            "vlan": 103,
            "voiceVlan": None,
            "allowedVlans": "all",
            "activeVlans": "1-4094",
            "isolationEnabled": False,
            "rstpEnabled": True,
            "stpGuard": "disabled",
            "linkNegotiation": "Auto negotiate",
            "portScheduleId": None,
            "schedule": None,
            "udld": "Alert only",
            "accessPolicyType": "Open",
            "daiTrusted": False,
            "profile": {
                "enabled": False,
                "id": "",
                "iname": None
            },
            "module": {
                "model": None
            },
            "mirror": {
                "mode": "Not mirroring traffic"
            }
         }
    },
    "uplink": {
        "priority": 50,
        "pattern": r"(uplink|trunk|core)",
        "payload": {
            "tags": [],
            "enabled": True,
            "poeEnabled": False,
            "type": "trunk",
            "vlan": 1,
            "voiceVlan": None,
            "allowedVlans": "all",
            "isolationEnabled": False,
            "rstpEnabled": True,
            "stpGuard": "disabled",
            "linkNegotiation": "Auto negotiate",
            "portScheduleId": None,
            "schedule": None,
            "udld": "Alert only",
            "accessPolicyType": "Open",
            "daiTrusted": False,
            "profile": {
                "enabled": False,
                "id": "",
                "iname": None
            },
            "module": {
                "model": None
            },
            "mirror": {
                "mode": "Not mirroring traffic"
            }
        }
    }
}

PORT_PROFILES_ENT = {
    "firewall_lan": {
        "priority": 100,
        "pattern": r"firewall.*lan|lan.*firewall",
        "payload": {
            "tags": [],
            "enabled": False,
            "poeEnabled": False,
            "type": "trunk",
            "vlan": 1,
            "voiceVlan": None,
            "allowedVlans": "301-304,306,307,311,312,320,321,323-325",
            "activeVlans": "301-304,306-307,311-312,320-321,323-325",
            "isolationEnabled": False,
            "rstpEnabled": False,
            "stpGuard": "disabled",
            "linkNegotiation": "Auto negotiate",
            "portScheduleId": None,
            "schedule": None,
            "udld": "Alert only",
            "accessPolicyType": "Open",
            "daiTrusted": False,
            "profile": {
                "enabled": False,
                "id": "",
                "iname": None
            },
            "module": {
                "model": None    
            },
            "mirror": {
                "mode": "Not mirroring traffic"
            }
        }
    },
    "ap|ponteradio--Trunk-vlan307": {
        "priority": 90,
        "pattern": r"^(ap.*|.*uplink_bridge.*)$",
        "payload": {
            "tags": [],
            "enabled": True,
            "poeEnabled": True,
            "type": "trunk",
            "vlan": 307,
            "voiceVlan": None,
            "allowedVlans": "304,306,307,320,503,504,523",
            "activeVlans": "304,306,307,320,503,504,523",
            "isolationEnabled": False,
            "rstpEnabled": True,
            "stpGuard": "disabled",
            "linkNegotiation": "Auto negotiate",
            "portScheduleId": None,
            "schedule": None,
            "udld": "Alert only",
            "accessPolicyType": "Open",
            "daiTrusted": False,
            "profile": {
                "enabled": False,
                "id": "",
                "iname": None
            },
            "module": {
                "model": None
            },
            "mirror": {
                "mode": "Not mirroring traffic"
            }
         }
    },
    "client-vlan304": {
        "priority": 60,
        "pattern": r"\b(client/|monitor/)\b",
        "payload": {
            "tags": [],
            "enabled": True,
            "poeEnabled": False,
            "type": "access",
            "vlan": 304,
            "voiceVlan": None,
            "allowedVlans": "all",
            "activeVlans": "1-4094",
            "isolationEnabled": False,
            "rstpEnabled": True,
            "stpGuard": "disabled",
            "linkNegotiation": "Auto negotiate",
            "portScheduleId": None,
            "schedule": None,
            "udld": "Alert only",
            "accessPolicyType": "Open",
            "daiTrusted": False,
            "profile": {
                "enabled": False,
                "id": "",
                "iname": None
            },
            "module": {
                "model": None
            },
            "mirror": {
                "mode": "Not mirroring traffic"
            }
         }
    },
    "b2c-vlan325": {
        "priority": 60,
        "pattern": r"\b(b2c/)\b",
        "payload": {
            "tags": [],
            "enabled": True,
            "poeEnabled": False,
            "type": "access",
            "vlan": 503,
            "voiceVlan": None,
            "allowedVlans": "all",
            "activeVlans": "1-4094",
            "isolationEnabled": False,
            "rstpEnabled": True,
            "stpGuard": "disabled",
            "linkNegotiation": "Auto negotiate",
            "portScheduleId": None,
            "schedule": None,
            "udld": "Alert only",
            "accessPolicyType": "Open",
            "daiTrusted": False,
            "profile": {
                "enabled": False,
                "id": "",
                "iname": None
            },
            "module": {
                "model": None
            },
            "mirror": {
                "mode": "Not mirroring traffic"
            }
         }
    },
    "fornitori-vlan302": {
        "priority": 60,
        "pattern": r"\b(fornitori/|pagodil)\b",
        "payload": {
            "tags": [],
            "enabled": True,
            "poeEnabled": False,
            "type": "access",
            "vlan": 302,
            "voiceVlan": None,
            "allowedVlans": "all",
            "activeVlans": "1-4094",
            "isolationEnabled": False,
            "rstpEnabled": True,
            "stpGuard": "disabled",
            "linkNegotiation": "Auto negotiate",
            "portScheduleId": None,
            "schedule": None,
            "udld": "Alert only",
            "accessPolicyType": "Open",
            "daiTrusted": False,
            "profile": {
                "enabled": False,
                "id": "",
                "iname": None
            },
            "module": {
                "model": None
            },
            "mirror": {
                "mode": "Not mirroring traffic"
            }
         }
    },
    "printer-vlan306": {
        "priority": 60,
        "pattern": r"\b(printer/)\b",
        "payload": {
            "tags": [],
            "enabled": True,
            "poeEnabled": False,
            "type": "access",
            "vlan": 306,
            "voiceVlan": None,
            "allowedVlans": "all",
            "activeVlans": "1-4094",
            "isolationEnabled": False,
            "rstpEnabled": True,
            "stpGuard": "disabled",
            "linkNegotiation": "Auto negotiate",
            "portScheduleId": None,
            "schedule": None,
            "udld": "Alert only",
            "accessPolicyType": "Open",
            "daiTrusted": False,
            "profile": {
                "enabled": False,
                "id": "",
                "iname": None
            },
            "module": {
                "model": None
            },
            "mirror": {
                "mode": "Not mirroring traffic"
            }
         }
    },
    "tvcc-facility-vlan311": {
        "priority": 60,
        "pattern": r"\b(tvcc/|facility/)\b",
        "payload": {
            "tags": [],
            "enabled": True,
            "poeEnabled": True,
            "type": "access",
            "vlan": 311,
            "voiceVlan": None,
            "allowedVlans": "all",
            "activeVlans": "1-4094",
            "isolationEnabled": False,
            "rstpEnabled": True,
            "stpGuard": "disabled",
            "linkNegotiation": "Auto negotiate",
            "portScheduleId": None,
            "schedule": None,
            "udld": "Alert only",
            "accessPolicyType": "Open",
            "daiTrusted": False,
            "profile": {
                "enabled": False,
                "id": "",
                "iname": None
            },
            "module": {
                "model": None
            },
            "mirror": {
                "mode": "Not mirroring traffic"
            }
         }
    },
    "disable-by-user": {
        "priority": 40,
        "pattern": r"^\*{3}",
        "payload": {
            "tags": [],
            "enabled": False,
            "poeEnabled": False,
            "type": "access",
            "vlan": 1,
            "voiceVlan": None,
            "allowedVlans": "all",
            "activeVlans": "1,101-103,301-304,306-307,311-312,320-321,323-325",
            "isolationEnabled": False,
            "rstpEnabled": True,
            "stpGuard": "disabled",
            "linkNegotiation": "Auto negotiate",
            "portScheduleId": None,
            "schedule": None,
            "udld": "Alert only",
            "accessPolicyType": "Open",
            "daiTrusted": False,
            "profile": {
                "enabled": False,
                "id": "",
                "iname": None
            },
            "module": {
                "model": None
            },
            "mirror": {
                "mode": "Not mirroring traffic"
            }
         }
    },
    "shut": {
        "priority": 40,
        "payload": {
            "tags": [],
            "enabled": False,
            "poeEnabled": False,
            "type": "access",
            "vlan": 1,
            "voiceVlan": None,
            "allowedVlans": "all",
            "activeVlans": "1,101-103,301-304,306-307,311-312,320-321,323-325",
            "isolationEnabled": False,
            "rstpEnabled": True,
            "stpGuard": "disabled",
            "linkNegotiation": "Auto negotiate",
            "portScheduleId": None,
            "schedule": None,
            "udld": "Alert only",
            "accessPolicyType": "Open",
            "daiTrusted": False,
            "profile": {
                "enabled": False,
                "id": "",
                "iname": None
            },
            "module": {
                "model": None
            },
            "mirror": {
                "mode": "Not mirroring traffic"
            }
         }
    },
    "wan-3-fex-vlan103": {
        "priority": 60,
        "pattern": r"\b(fex|rtr-wan-3)\b",
        "payload": {
            "tags": [],
            "enabled": True,
            "poeEnabled": True,
            "type": "access",
            "vlan": 103,
            "voiceVlan": None,
            "allowedVlans": "all",
            "activeVlans": "1-4094",
            "isolationEnabled": False,
            "rstpEnabled": True,
            "stpGuard": "disabled",
            "linkNegotiation": "Auto negotiate",
            "portScheduleId": None,
            "schedule": None,
            "udld": "Alert only",
            "accessPolicyType": "Open",
            "daiTrusted": False,
            "profile": {
                "enabled": False,
                "id": "",
                "iname": None
            },
            "module": {
                "model": None
            },
            "mirror": {
                "mode": "Not mirroring traffic"
            }
         }
    },
    "uplink": {
        "priority": 50,
        "pattern": r"(uplink|trunk|core)",
        "payload": {
            "tags": [],
            "enabled": True,
            "poeEnabled": False,
            "type": "trunk",
            "vlan": 1,
            "voiceVlan": None,
            "allowedVlans": "all",
            "isolationEnabled": False,
            "rstpEnabled": True,
            "stpGuard": "disabled",
            "linkNegotiation": "Auto negotiate",
            "portScheduleId": None,
            "schedule": None,
            "udld": "Alert only",
            "accessPolicyType": "Open",
            "daiTrusted": False,
            "profile": {
                "enabled": False,
                "id": "",
                "iname": None
            },
            "module": {
                "model": None
            },
            "mirror": {
                "mode": "Not mirroring traffic"
            }
        }
    }
}

PORT_PROFILES_RDC = {
    "firewall_lan": {
        "priority": 100,
        "pattern": r"firewall.*lan|lan.*firewall",
        "payload": {
            "tags": [],
            "enabled": False,
            "poeEnabled": False,
            "type": "trunk",
            "vlan": 1,
            "voiceVlan": None,
            "allowedVlans": "301-304,306,307,311,312,320,321,323-325",
            "activeVlans": "301-304,306-307,311-312,320-321,323-325",
            "isolationEnabled": False,
            "rstpEnabled": False,
            "stpGuard": "disabled",
            "linkNegotiation": "Auto negotiate",
            "portScheduleId": None,
            "schedule": None,
            "udld": "Alert only",
            "accessPolicyType": "Open",
            "daiTrusted": False,
            "profile": {
                "enabled": False,
                "id": "",
                "iname": None
            },
            "module": {
                "model": None    
            },
            "mirror": {
                "mode": "Not mirroring traffic"
            }
        }
    },
    "ap|ponteradio--Trunk-vlan307": {
        "priority": 90,
        "pattern": r"ap\d+|.*uplink_bridge.*",
        "payload": {
            "tags": [],
            "enabled": True,
            "poeEnabled": True,
            "type": "trunk",
            "vlan": 307,
            "voiceVlan": None,
            "allowedVlans": "304,306-307,320",
            "activeVlans": "304,306-307,320",
            "isolationEnabled": False,
            "rstpEnabled": True,
            "stpGuard": "disabled",
            "linkNegotiation": "Auto negotiate",
            "portScheduleId": None,
            "schedule": None,
            "udld": "Alert only",
            "accessPolicyType": "Open",
            "daiTrusted": False,
            "profile": {
                "enabled": False,
                "id": "",
                "iname": None
            },
            "module": {
                "model": None
            },
            "mirror": {
                "mode": "Not mirroring traffic"
            }
         }
    },
    "cassa-vlan301": {
        "priority": 50,
        "pattern": r"\b(cassa/)\b",
        "payload": {
            "tags": [],
            "enabled": True,
            "poeEnabled": False,
            "type": "access",
            "vlan": 301,
            "voiceVlan": None,
            "allowedVlans": "all",
            "activeVlans": "1-4094",
            "isolationEnabled": False,
            "rstpEnabled": True,
            "stpGuard": "disabled",
            "linkNegotiation": "Auto negotiate",
            "portScheduleId": None,
            "schedule": None,
            "udld": "Alert only",
            "accessPolicyType": "Open",
            "daiTrusted": False,
            "profile": {
                "enabled": False,
                "id": "",
                "iname": None
            },
            "module": {
                "model": None
            },
            "mirror": {
                "mode": "Not mirroring traffic"
            }
         }
    },
    "strongbox-vlan312": {
        "priority": 50,
        "pattern": r"\b(strongbox/)\b",
        "payload": {
            "tags": [],
            "enabled": True,
            "poeEnabled": False,
            "type": "access",
            "vlan": 312,
            "voiceVlan": None,
            "allowedVlans": "all",
            "activeVlans": "1-4094",
            "isolationEnabled": False,
            "rstpEnabled": True,
            "stpGuard": "disabled",
            "linkNegotiation": "Auto negotiate",
            "portScheduleId": None,
            "schedule": None,
            "udld": "Alert only",
            "accessPolicyType": "Open",
            "daiTrusted": False,
            "profile": {
                "enabled": False,
                "id": "",
                "iname": None
            },
            "module": {
                "model": None
            },
            "mirror": {
                "mode": "Not mirroring traffic"
            }
         }
    },
    "client-vlan304": {
        "priority": 60,
        "pattern": r"\b(client/|monitor/)\b",
        "payload": {
            "tags": [],
            "enabled": True,
            "poeEnabled": False,
            "type": "access",
            "vlan": 304,
            "voiceVlan": None,
            "allowedVlans": "all",
            "activeVlans": "1-4094",
            "isolationEnabled": False,
            "rstpEnabled": True,
            "stpGuard": "disabled",
            "linkNegotiation": "Auto negotiate",
            "portScheduleId": None,
            "schedule": None,
            "udld": "Alert only",
            "accessPolicyType": "Open",
            "daiTrusted": False,
            "profile": {
                "enabled": False,
                "id": "",
                "iname": None
            },
            "module": {
                "model": None
            },
            "mirror": {
                "mode": "Not mirroring traffic"
            }
         }
    },
    "bms-vlan325": {
        "priority": 60,
        "pattern": r"\b(bms/)\b",
        "payload": {
            "tags": [],
            "enabled": True,
            "poeEnabled": False,
            "type": "access",
            "vlan": 325,
            "voiceVlan": None,
            "allowedVlans": "all",
            "activeVlans": "1-4094",
            "isolationEnabled": False,
            "rstpEnabled": True,
            "stpGuard": "disabled",
            "linkNegotiation": "Auto negotiate",
            "portScheduleId": None,
            "schedule": None,
            "udld": "Alert only",
            "accessPolicyType": "Open",
            "daiTrusted": False,
            "profile": {
                "enabled": False,
                "id": "",
                "iname": None
            },
            "module": {
                "model": None
            },
            "mirror": {
                "mode": "Not mirroring traffic"
            }
         }
    },
    "fornitori-vlan302": {
        "priority": 60,
        "pattern": r"\b(fornitori/|pagodil)\b",
        "payload": {
            "tags": [],
            "enabled": True,
            "poeEnabled": False,
            "type": "access",
            "vlan": 302,
            "voiceVlan": None,
            "allowedVlans": "all",
            "activeVlans": "1-4094",
            "isolationEnabled": False,
            "rstpEnabled": True,
            "stpGuard": "disabled",
            "linkNegotiation": "Auto negotiate",
            "portScheduleId": None,
            "schedule": None,
            "udld": "Alert only",
            "accessPolicyType": "Open",
            "daiTrusted": False,
            "profile": {
                "enabled": False,
                "id": "",
                "iname": None
            },
            "module": {
                "model": None
            },
            "mirror": {
                "mode": "Not mirroring traffic"
            }
         }
    },
    "printer-vlan306": {
        "priority": 60,
        "pattern": r"\b(printer/)\b",
        "payload": {
            "tags": [],
            "enabled": True,
            "poeEnabled": False,
            "type": "access",
            "vlan": 306,
            "voiceVlan": None,
            "allowedVlans": "all",
            "activeVlans": "1-4094",
            "isolationEnabled": False,
            "rstpEnabled": True,
            "stpGuard": "disabled",
            "linkNegotiation": "Auto negotiate",
            "portScheduleId": None,
            "schedule": None,
            "udld": "Alert only",
            "accessPolicyType": "Open",
            "daiTrusted": False,
            "profile": {
                "enabled": False,
                "id": "",
                "iname": None
            },
            "module": {
                "model": None
            },
            "mirror": {
                "mode": "Not mirroring traffic"
            }
         }
    },
    "tvcc-vlan311": {
        "priority": 60,
        "pattern": r"\b(tvcc/|facility/)\b",
        "payload": {
            "tags": [],
            "enabled": True,
            "poeEnabled": True,
            "type": "access",
            "vlan": 311,
            "voiceVlan": None,
            "allowedVlans": "all",
            "activeVlans": "1-4094",
            "isolationEnabled": False,
            "rstpEnabled": True,
            "stpGuard": "disabled",
            "linkNegotiation": "Auto negotiate",
            "portScheduleId": None,
            "schedule": None,
            "udld": "Alert only",
            "accessPolicyType": "Open",
            "daiTrusted": False,
            "profile": {
                "enabled": False,
                "id": "",
                "iname": None
            },
            "module": {
                "model": None
            },
            "mirror": {
                "mode": "Not mirroring traffic"
            }
         }
    },
    "disable-by-user": {
        "priority": 40,
        "pattern": r"^\*{3}",
        "payload": {
            "tags": [],
            "enabled": False,
            "poeEnabled": False,
            "type": "access",
            "vlan": 1,
            "voiceVlan": None,
            "allowedVlans": "all",
            "activeVlans": "1,101-103,301-304,306-307,311-312,320-321,323-325",
            "isolationEnabled": False,
            "rstpEnabled": True,
            "stpGuard": "disabled",
            "linkNegotiation": "Auto negotiate",
            "portScheduleId": None,
            "schedule": None,
            "udld": "Alert only",
            "accessPolicyType": "Open",
            "daiTrusted": False,
            "profile": {
                "enabled": False,
                "id": "",
                "iname": None
            },
            "module": {
                "model": None
            },
            "mirror": {
                "mode": "Not mirroring traffic"
            }
         }
    },
    "shut": {
        "priority": 40,
        "payload": {
            "tags": [],
            "enabled": False,
            "poeEnabled": False,
            "type": "access",
            "vlan": 1,
            "voiceVlan": None,
            "allowedVlans": "all",
            "activeVlans": "1,101-103,301-304,306-307,311-312,320-321,323-325",
            "isolationEnabled": False,
            "rstpEnabled": True,
            "stpGuard": "disabled",
            "linkNegotiation": "Auto negotiate",
            "portScheduleId": None,
            "schedule": None,
            "udld": "Alert only",
            "accessPolicyType": "Open",
            "daiTrusted": False,
            "profile": {
                "enabled": False,
                "id": "",
                "iname": None
            },
            "module": {
                "model": None
            },
            "mirror": {
                "mode": "Not mirroring traffic"
            }
         }
    },
    "wan-3-fex-vlan103": {
        "priority": 60,
        "pattern": r"\b(fex|rtr-wan-3)\b",
        "payload": {
            "tags": [],
            "enabled": True,
            "poeEnabled": True,
            "type": "access",
            "vlan": 103,
            "voiceVlan": None,
            "allowedVlans": "all",
            "activeVlans": "1-4094",
            "isolationEnabled": False,
            "rstpEnabled": True,
            "stpGuard": "disabled",
            "linkNegotiation": "Auto negotiate",
            "portScheduleId": None,
            "schedule": None,
            "udld": "Alert only",
            "accessPolicyType": "Open",
            "daiTrusted": False,
            "profile": {
                "enabled": False,
                "id": "",
                "iname": None
            },
            "module": {
                "model": None
            },
            "mirror": {
                "mode": "Not mirroring traffic"
            }
         }
    },
    "uplink": {
        "priority": 50,
        "pattern": r"(uplink|trunk|core)",
        "payload": {
            "tags": [],
            "enabled": True,
            "poeEnabled": False,
            "type": "trunk",
            "vlan": 1,
            "voiceVlan": None,
            "allowedVlans": "all",
            "isolationEnabled": False,
            "rstpEnabled": True,
            "stpGuard": "disabled",
            "linkNegotiation": "Auto negotiate",
            "portScheduleId": None,
            "schedule": None,
            "udld": "Alert only",
            "accessPolicyType": "Open",
            "daiTrusted": False,
            "profile": {
                "enabled": False,
                "id": "",
                "iname": None
            },
            "module": {
                "model": None
            },
            "mirror": {
                "mode": "Not mirroring traffic"
            }
        }
    }
}

PORT_PROFILES_SRM = {
    "firewall_lan": {
        "priority": 100,
        "pattern": r"firewall.*lan|lan.*firewall",
        "payload": {
            "tags": [],
            "enabled": False,
            "poeEnabled": False,
            "type": "trunk",
            "vlan": 1,
            "voiceVlan": None,
            "allowedVlans": "301-304,306,307,311,312,320,321,323-325",
            "activeVlans": "301-304,306-307,311-312,320-321,323-325",
            "isolationEnabled": False,
            "rstpEnabled": False,
            "stpGuard": "disabled",
            "linkNegotiation": "Auto negotiate",
            "portScheduleId": None,
            "schedule": None,
            "udld": "Alert only",
            "accessPolicyType": "Open",
            "daiTrusted": False,
            "profile": {
                "enabled": False,
                "id": "",
                "iname": None
            },
            "module": {
                "model": None    
            },
            "mirror": {
                "mode": "Not mirroring traffic"
            }
        }
    },
    "ap|ponteradio--Trunk-vlan307": {
        "priority": 90,
        "pattern": r"ap\d+|.*uplink_bridge.*",
        "payload": {
            "tags": [],
            "enabled": True,
            "poeEnabled": True,
            "type": "trunk",
            "vlan": 307,
            "voiceVlan": None,
            "allowedVlans": "304,306-307,320,323",
            "activeVlans": "304,306-307,320,323",
            "isolationEnabled": False,
            "rstpEnabled": True,
            "stpGuard": "disabled",
            "linkNegotiation": "Auto negotiate",
            "portScheduleId": None,
            "schedule": None,
            "udld": "Alert only",
            "accessPolicyType": "Open",
            "daiTrusted": False,
            "profile": {
                "enabled": False,
                "id": "",
                "iname": None
            },
            "module": {
                "model": None
            },
            "mirror": {
                "mode": "Not mirroring traffic"
            }
         }
    },
    "aplabel-vlan307": {
        "priority": 50,
        "pattern": r"\b(aplabel/)\b",
        "payload": {
            "tags": [],
            "enabled": True,
            "poeEnabled": True,
            "type": "access",
            "vlan": 307,
            "voiceVlan": None,
            "allowedVlans": "all",
            "activeVlans": "1-4094",
            "isolationEnabled": False,
            "rstpEnabled": True,
            "stpGuard": "disabled",
            "linkNegotiation": "Auto negotiate",
            "portScheduleId": None,
            "schedule": None,
            "udld": "Alert only",
            "accessPolicyType": "Open",
            "daiTrusted": False,
            "profile": {
                "enabled": False,
                "id": "",
                "iname": None
            },
            "module": {
                "model": None
            },
            "mirror": {
                "mode": "Not mirroring traffic"
            }
         }
    },
    "cassa-vlan301": {
        "priority": 50,
        "pattern": r"\b(cassa/)\b",
        "payload": {
            "tags": [],
            "enabled": True,
            "poeEnabled": False,
            "type": "access",
            "vlan": 301,
            "voiceVlan": None,
            "allowedVlans": "all",
            "activeVlans": "1-4094",
            "isolationEnabled": False,
            "rstpEnabled": True,
            "stpGuard": "disabled",
            "linkNegotiation": "Auto negotiate",
            "portScheduleId": None,
            "schedule": None,
            "udld": "Alert only",
            "accessPolicyType": "Open",
            "daiTrusted": False,
            "profile": {
                "enabled": False,
                "id": "",
                "iname": None
            },
            "module": {
                "model": None
            },
            "mirror": {
                "mode": "Not mirroring traffic"
            }
         }
    },
    "cash-new-vlan321": {
        "priority": 50,
        "pattern": r"\b(cash-new/)\b",
        "payload": {
            "tags": [],
            "enabled": True,
            "poeEnabled": False,
            "type": "access",
            "vlan": 321,
            "voiceVlan": None,
            "allowedVlans": "all",
            "activeVlans": "1-4094",
            "isolationEnabled": False,
            "rstpEnabled": True,
            "stpGuard": "disabled",
            "linkNegotiation": "Auto negotiate",
            "portScheduleId": None,
            "schedule": None,
            "udld": "Alert only",
            "accessPolicyType": "Open",
            "daiTrusted": False,
            "profile": {
                "enabled": False,
                "id": "",
                "iname": None
            },
            "module": {
                "model": None
            },
            "mirror": {
                "mode": "Not mirroring traffic"
            }
         }
    },
    "strongbox-vlan312": {
        "priority": 50,
        "pattern": r"\b(strongbox/)\b",
        "payload": {
            "tags": [],
            "enabled": True,
            "poeEnabled": False,
            "type": "access",
            "vlan": 312,
            "voiceVlan": None,
            "allowedVlans": "all",
            "activeVlans": "1-4094",
            "isolationEnabled": False,
            "rstpEnabled": True,
            "stpGuard": "disabled",
            "linkNegotiation": "Auto negotiate",
            "portScheduleId": None,
            "schedule": None,
            "udld": "Alert only",
            "accessPolicyType": "Open",
            "daiTrusted": False,
            "profile": {
                "enabled": False,
                "id": "",
                "iname": None
            },
            "module": {
                "model": None
            },
            "mirror": {
                "mode": "Not mirroring traffic"
            }
         }
    },
    "client-vlan304": {
        "priority": 60,
        "pattern": r"\b(client/|monitor/)\b",
        "payload": {
            "tags": [],
            "enabled": True,
            "poeEnabled": False,
            "type": "access",
            "vlan": 304,
            "voiceVlan": None,
            "allowedVlans": "all",
            "activeVlans": "1-4094",
            "isolationEnabled": False,
            "rstpEnabled": True,
            "stpGuard": "disabled",
            "linkNegotiation": "Auto negotiate",
            "portScheduleId": None,
            "schedule": None,
            "udld": "Alert only",
            "accessPolicyType": "Open",
            "daiTrusted": False,
            "profile": {
                "enabled": False,
                "id": "",
                "iname": None
            },
            "module": {
                "model": None
            },
            "mirror": {
                "mode": "Not mirroring traffic"
            }
         }
    },
    "bms-vlan325": {
        "priority": 60,
        "pattern": r"\b(bms/)\b",
        "payload": {
            "tags": [],
            "enabled": True,
            "poeEnabled": False,
            "type": "access",
            "vlan": 325,
            "voiceVlan": None,
            "allowedVlans": "all",
            "activeVlans": "1-4094",
            "isolationEnabled": False,
            "rstpEnabled": True,
            "stpGuard": "disabled",
            "linkNegotiation": "Auto negotiate",
            "portScheduleId": None,
            "schedule": None,
            "udld": "Alert only",
            "accessPolicyType": "Open",
            "daiTrusted": False,
            "profile": {
                "enabled": False,
                "id": "",
                "iname": None
            },
            "module": {
                "model": None
            },
            "mirror": {
                "mode": "Not mirroring traffic"
            }
         }
    },
    "fornitori-vlan302": {
        "priority": 60,
        "pattern": r"\b(fornitori/|pagodil)\b",
        "payload": {
            "tags": [],
            "enabled": True,
            "poeEnabled": False,
            "type": "access",
            "vlan": 302,
            "voiceVlan": None,
            "allowedVlans": "all",
            "activeVlans": "1-4094",
            "isolationEnabled": False,
            "rstpEnabled": True,
            "stpGuard": "disabled",
            "linkNegotiation": "Auto negotiate",
            "portScheduleId": None,
            "schedule": None,
            "udld": "Alert only",
            "accessPolicyType": "Open",
            "daiTrusted": False,
            "profile": {
                "enabled": False,
                "id": "",
                "iname": None
            },
            "module": {
                "model": None
            },
            "mirror": {
                "mode": "Not mirroring traffic"
            }
         }
    },
    "printer-vlan306": {
        "priority": 60,
        "pattern": r"\b(printer/)\b",
        "payload": {
            "tags": [],
            "enabled": True,
            "poeEnabled": False,
            "type": "access",
            "vlan": 306,
            "voiceVlan": None,
            "allowedVlans": "all",
            "activeVlans": "1-4094",
            "isolationEnabled": False,
            "rstpEnabled": True,
            "stpGuard": "disabled",
            "linkNegotiation": "Auto negotiate",
            "portScheduleId": None,
            "schedule": None,
            "udld": "Alert only",
            "accessPolicyType": "Open",
            "daiTrusted": False,
            "profile": {
                "enabled": False,
                "id": "",
                "iname": None
            },
            "module": {
                "model": None
            },
            "mirror": {
                "mode": "Not mirroring traffic"
            }
         }
    },
    "tvcc-vlan311": {
        "priority": 60,
        "pattern": r"\b(tvcc/|facility/)\b",
        "payload": {
            "tags": [],
            "enabled": True,
            "poeEnabled": True,
            "type": "access",
            "vlan": 311,
            "voiceVlan": None,
            "allowedVlans": "all",
            "activeVlans": "1-4094",
            "isolationEnabled": False,
            "rstpEnabled": True,
            "stpGuard": "disabled",
            "linkNegotiation": "Auto negotiate",
            "portScheduleId": None,
            "schedule": None,
            "udld": "Alert only",
            "accessPolicyType": "Open",
            "daiTrusted": False,
            "profile": {
                "enabled": False,
                "id": "",
                "iname": None
            },
            "module": {
                "model": None
            },
            "mirror": {
                "mode": "Not mirroring traffic"
            }
         }
    },
    "disable-by-user": {
        "priority": 40,
        "pattern": r"^\*{3}",
        "payload": {
            "tags": [],
            "enabled": False,
            "poeEnabled": False,
            "type": "access",
            "vlan": 1,
            "voiceVlan": None,
            "allowedVlans": "all",
            "activeVlans": "1,101-103,301-304,306-307,311-312,320-321,323-325",
            "isolationEnabled": False,
            "rstpEnabled": True,
            "stpGuard": "disabled",
            "linkNegotiation": "Auto negotiate",
            "portScheduleId": None,
            "schedule": None,
            "udld": "Alert only",
            "accessPolicyType": "Open",
            "daiTrusted": False,
            "profile": {
                "enabled": False,
                "id": "",
                "iname": None
            },
            "module": {
                "model": None
            },
            "mirror": {
                "mode": "Not mirroring traffic"
            }
         }
    },
    "shut": {
        "priority": 40,
        "payload": {
            "tags": [],
            "enabled": False,
            "poeEnabled": False,
            "type": "access",
            "vlan": 1,
            "voiceVlan": None,
            "allowedVlans": "all",
            "activeVlans": "1,101-103,301-304,306-307,311-312,320-321,323-325",
            "isolationEnabled": False,
            "rstpEnabled": True,
            "stpGuard": "disabled",
            "linkNegotiation": "Auto negotiate",
            "portScheduleId": None,
            "schedule": None,
            "udld": "Alert only",
            "accessPolicyType": "Open",
            "daiTrusted": False,
            "profile": {
                "enabled": False,
                "id": "",
                "iname": None
            },
            "module": {
                "model": None
            },
            "mirror": {
                "mode": "Not mirroring traffic"
            }
         }
    },
    "wan-3-fex-vlan103": {
        "priority": 60,
        "pattern": r"\b(fex|rtr-wan-3)\b",
        "payload": {
            "tags": [],
            "enabled": True,
            "poeEnabled": True,
            "type": "access",
            "vlan": 103,
            "voiceVlan": None,
            "allowedVlans": "all",
            "activeVlans": "1-4094",
            "isolationEnabled": False,
            "rstpEnabled": True,
            "stpGuard": "disabled",
            "linkNegotiation": "Auto negotiate",
            "portScheduleId": None,
            "schedule": None,
            "udld": "Alert only",
            "accessPolicyType": "Open",
            "daiTrusted": False,
            "profile": {
                "enabled": False,
                "id": "",
                "iname": None
            },
            "module": {
                "model": None
            },
            "mirror": {
                "mode": "Not mirroring traffic"
            }
         }
    },
    "uplink": {
        "priority": 50,
        "pattern": r"(uplink|trunk|core)",
        "payload": {
            "tags": [],
            "enabled": True,
            "poeEnabled": False,
            "type": "trunk",
            "vlan": 1,
            "voiceVlan": None,
            "allowedVlans": "all",
            "isolationEnabled": False,
            "rstpEnabled": True,
            "stpGuard": "disabled",
            "linkNegotiation": "Auto negotiate",
            "portScheduleId": None,
            "schedule": None,
            "udld": "Alert only",
            "accessPolicyType": "Open",
            "daiTrusted": False,
            "profile": {
                "enabled": False,
                "id": "",
                "iname": None
            },
            "module": {
                "model": None
            },
            "mirror": {
                "mode": "Not mirroring traffic"
            }
        }
    }
}