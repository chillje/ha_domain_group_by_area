from homeassistant.helpers import device_registry as dr
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers import area_registry as ar

def get_all_areas():
    try:
        areareg = ar.async_get(hass)

        all_areas = [entry.id.lower() for id, entry in areareg.areas.items()]

        return all_areas

    except Exception as e:
        log.error(f"Error getting all areas: {e}")
        return []

def get_area_entities(area_name, domain):
    try:
        devreg = dr.async_get(hass)
        entreg = er.async_get(hass)
        area_entities = []

        for d in devreg.devices.items():
            device_id = d[0]
            device_entry = d[1]

            if device_entry.area_id and area_name in device_entry.area_id:
                desired_entity_id = device_entry.id

                for ent in entreg.entities.items():
                    entity_id = ent[0]
                    entity_entry = ent[1]

                    if entity_entry.device_id and desired_entity_id in entity_entry.device_id:
                        if entity_entry.entity_id.startswith(f"{domain}."):
                            if entity_entry.disabled_by is None and entity_entry.hidden_by is None:
                                area_entities.append(entity_entry.entity_id.strip())
                            else:
                                log.debug(f"Entry is disabled or hidden: {entity_entry.entity_id}")

        return area_entities

    except Exception as e:
        log.error(f"Error getting area entities: {e}")
        return []

def filter_entity_blacklist(entities, blacklist):
    try:
        log.debug(f"Filter blacklisted entities: {blacklist}")

        if blacklist is None:
            filtered_entities = entities
        else:
            filtered_entities = [entity for entity in entities if entity not in blacklist]

        log.debug(f"Filtered entities: {filtered_entities}")
        return filtered_entities

    except Exception as e:
        log.error(f"Error filtering entity_blacklist: {e}")
        return entities

def filter_platform_blacklist(entities, blacklist):
    try:
        log.debug(f"Filter blacklisted platforms: {blacklist}")

        if blacklist is None:
            filtered_entities = entities
        else:
            entreg = er.async_get(hass)
            filtered_entities = []
            for ent in entreg.entities.items():
                entity_id = ent[0]
                entity_entry = ent[1]
            
                for entity in entities:
                    if entity_entry.entity_id in entity:
                        if entity_entry.platform not in blacklist:
                            filtered_entities.append(entity)

        log.debug(f"Filtered platforms: {filtered_entities}")
        return filtered_entities

    except Exception as e:
        log.error(f"Error filtering platform_blacklist: {e}")
        return entities

def process_area(area_name, domain, entity_blacklist, platform_blacklist):
    try:
        group_name = f"area_{area_name}_all_{domain}s"
        area_domain_entities = get_area_entities(area_name, domain)

        if len(area_domain_entities) > 0:
            filtered_domain_entities = filter_entity_blacklist(area_domain_entities, entity_blacklist)
        else:
            filtered_domain_entities = area_domain_entities

        if len(filtered_domain_entities) > 0:
            group_entities = filter_platform_blacklist(filtered_domain_entities, platform_blacklist)
        else:
            group_entities = filtered_domain_entities

        if len(group_entities) > 0:
            create_group(group_name, group_entities)
        else:
            delete_group(group_name)

    except Exception as e:
        log.error(f"Error processing area: {e}")

def create_group(group_name, entities):
    try:
        log.debug(f"Creating group: {group_name}")
        log.debug(f"Entities in the group: {entities}")

        # Create the group
        group.set(object_id=group_name, entities=entities)
    
    except Exception as e:
        log.error(f"Error creating group: {e}")

def delete_group(group_name):
    try:
        log.debug(f"Deleting group: {group_name}")

        # FIXME
        # This is ugly but at this time I cant find
        # another solution to test if a group exists.
        try:
            state.get(f"group.{group_name}")
            group.remove(object_id=group_name)
        except NameError as e:
            log.debug(f"Deleting group: {group_name} does not exist, skipping.")

    except Exception as e:
        log.error(f"Error deleting group: {e}")

def create_all(domain, entity_blacklist, platform_blacklist):
    try:
        group_name = f"all_{domain}s"
        log.debug(f"Create group: {group_name}")

        all_entities_of_domain = state.names(domain)
        filtered_domain_entities = filter_entity_blacklist(all_entities_of_domain, entity_blacklist)
        group_entities = filter_platform_blacklist(filtered_domain_entities, platform_blacklist)

        if group_entities:
            create_group(group_name, group_entities)
        else:
            delete_group(group_name)
        
    except Exception as e:
        log.error(f"Error creating \"all_domain\" group of domain: {e}")

@service
def domain_group_by_area(domain, entity_blacklist=None, area_whitelist=None, platform_blacklist=None, all=None):
    try:
        if not isinstance(domain, str) or not domain:
            log.error("Bad domain! Not executing.")
        else:
            log.debug(f"Loaded domain: {domain}")
            log.debug(f"Entity black list: {entity_blacklist}")

            if area_whitelist is None:
                all_areas = get_all_areas()
            else:
                all_areas = area_whitelist

            log.debug(f"List of areas: {all_areas}")

            for area_name in all_areas:
                process_area(area_name, domain, entity_blacklist, platform_blacklist)

            if all:
                create_all(domain, entity_blacklist, platform_blacklist)

    except Exception as e:
        log.error(f"Error in domain_group_by_area: {e}")
