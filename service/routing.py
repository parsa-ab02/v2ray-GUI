import copy

ROUTING_PROFILES: dict[str, dict] = {}

Routing_profile: dict | None = None

def get_profile():
    global Routing_profile
    return Routing_profile

def set_profile(profile: dict | None = None,name: str | None = None):
    global Routing_profile
    if name is not None and profile is None:
        try:
            Routing_profile = get_routing(profile_name=name)
        except ValueError as e:
            return f"error: {e}"

    elif name is None and profile is not None:
        add_profile(name = "costum profile", profile=profile)
        Routing_profile = profile

    else:
        raise ValueError("just enter profile name or enter new profile")

def add_profile(name:str, profile: dict):
    ROUTING_PROFILES.update({name:profile})

def get_routing(profile_name: str = "full_tunnel") -> dict:
    profile = ROUTING_PROFILES.get(profile_name)

    if profile is None:
        raise ValueError(f"Unknown routing profile: {profile_name}")

    return copy.deepcopy(profile)

def get_routing_profile_names() -> list:
    return list(ROUTING_PROFILES.keys())