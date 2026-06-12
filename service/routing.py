import copy

ROUTING_PROFILES = {
    "bypass_iran": {
        "domainStrategy": "AsIs",
        "rules": [
            {
                "type": "field",
                "domain": ["geosite:ir"],
                "outboundTag": "direct"
            },
            {
                "type": "field",
                "ip": ["geoip:ir"],
                "outboundTag": "direct"
            },
            {
                "type": "field",
                "ip": ["geoip:private"],
                "outboundTag": "direct"
            }
        ]
    },

    "full_tunnel": {
        "domainStrategy": "AsIs",
        "rules": []
    },

    "bypass_private": {
        "domainStrategy": "AsIs",
        "rules": [
            {
                "type": "field",
                "ip": ["geoip:private"],
                "outboundTag": "direct"
            }
        ]
    },

    "direct_all": {
        "domainStrategy": "AsIs",
        "rules": [
            {
                "type": "field",
                "network": "tcp,udp",
                "outboundTag": "direct"
            }
        ]
    }
}


def get_routing(profile_name: str = "full_tunnel") -> dict:
    profile = ROUTING_PROFILES.get(profile_name)

    if profile is None:
        raise ValueError(f"Unknown routing profile: {profile_name}")

    return copy.deepcopy(profile)


def get_routing_profile_names() -> list:
    return list(ROUTING_PROFILES.keys())