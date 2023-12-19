from homeassistant.helpers import device_registry as dr
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers import area_registry as ar

def get_all_areas():
    try:
        areareg = ar.async_get(hass)
        all_areas = []

        for a in areareg.areas.items():
            id = a[0]
            entry = a[1]
            log.info(f"Area: {entry.id} {entry.name} id: {id}")
            all_areas.append(entry.id)

        all_areas = [element.lower() for element in all_areas]
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
                                log.info(f"Entry is disabled or hidden: {entity_entry.entity_id}")

        return area_entities

    except Exception as e:
        log.error(f"Error getting area entities: {e}")
        return []

def filter_blacklist(entities, blacklist):
    try:
        log.debug(f"Filter blacklisted entries: {entities}")
        filtered_entities = [entity for entity in entities if entity not in blacklist]
        log.debug(f"Filtered area entries: {filtered_entities}")
        return filtered_entities

    except Exception as e:
        log.error(f"Error filtering blacklist: {e}")
        return entities

def process_area(area_name, domain, entity_blacklist):
    try:
        group_name = f"{area_name}_all_{domain}s"
        area_domain_entities = get_area_entities(area_name, domain)
        filtered_domain_entities = filter_blacklist(area_domain_entities, entity_blacklist)

        if len(filtered_domain_entities) > 0:
            create_group(group_name, filtered_domain_entities)
        #else:
        #    delete_group(group_name)

    except Exception as e:
        log.error(f"Error processing area: {e}")

def create_group(group_name, entities):
    try:
        log.info(f"Creating group: {group_name}")
        log.info(f"Entities in the group: {entities}")

        # Create the group
        group.set(object_id=group_name, entities=entities)
    
    except Exception as e:
        log.error(f"Error creating group: {e}")

def delete_group(group_name):
    try:
        log.info(f"Deleting group: {group_name}")

        # Remove the group
        #FIXME not working, state.get throws exception...
        #if state.get(f"group.{group_name}"):
        #    log.info(f"The group {group_name} exists. Deleting...")
        #    state.delete(f"group.{group_name}")

    except Exception as e:
        log.error(f"Error deleting group: {e}")

def create_all(domain, entity_blacklist):
    try:
        group_name = f"all_{domain}s"
        log.info(f"Create group: {group_name}")

        all_entities_of_domain = state.names(domain)
        filtered_domain_entities = filter_blacklist(all_entities_of_domain, entity_blacklist)

        if len(filtered_domain_entities) > 0:
            create_group(group_name, filtered_domain_entities)
        
    except Exception as e:
        log.error(f"Error creating \"all_domain\" group of domain: {e}")

@service
def domain_group_by_area(domain, entity_blacklist=None, area_whitelist=None, all=None):
    try:
        if not isinstance(domain, str) or not domain:
            log.error("Bad domain! Not executing.")
        else:
            log.info(f"Loaded domain: {domain}")
            log.info(f"Entity black list: {entity_blacklist}")

            if area_whitelist is None:
                all_areas = get_all_areas()
            else:
                all_areas = area_whitelist

            log.info(f"List of areas: {all_areas}")

            for area_name in all_areas:
                process_area(area_name, domain, entity_blacklist)

            if all:
                create_all(domain, entity_blacklist)

    except Exception as e:
        log.error(f"Error in domain_group_by_area: {e}")
