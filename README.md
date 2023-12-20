# ha_domain_group_by_area

This pyscript for home assistant will add configurable dynamic groups by domain per area.

The base idea was to have one group per domain for your several defined areas.
Lets say you will have one group of your light entities per area you can create them dynamically by now.
Just create an automation calling this pyscript-service and define some values needed for your dynamically created groups.

Example:
 - AREA1
   - `light.light1`
   - `light.light2`
   - `light.light3`
 - AREA2
   - `light.light1`
   - `light.light2`

Results to:
 * `group.area1_all_lights`
 * `group.area2_all_lights`

You can do this with other domains like "switch".

If you like my work, you can support me here:\
<a href="https://www.buymeacoffee.com/chillje" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>

## Feature list
:white_check_mark: Works with different domains (such as "light", "switch", ..)\
:white_check_mark: Automatic creation for all created areas\
:white_check_mark: Blacklist for single entities (optional)\
:white_check_mark: Whitelist for single areas (optional)\
:white_check_mark: Create an overall domain based group `group.all_lights`, `group.all_switchs` (optional)\
:white_square_button: Create groups for combined areas (AREA1 & AREA2)


## Prerequisites
- [pyscript](https://github.com/custom-components/pyscript) (easy to install via [HACS](https://hacs.xyz/))
- Pyscript needs to be configured "hass" as global variable:
  - UI:
    - HA Configuration -> Integrations -> Pyscript Python scripting -> configuration -> ""Home
      Assistant global variable"
  - *`configuration.yaml`*:
    ```
    pyscript:
      hass_is_global: true
    ```

## Installation
- Download/Clone this GitHub repository
- Copy folder *pyscript* to your HA instance config dir
  `config/pyscript/domain_group_by_area.py`
- Configuration for logging in *`configuration.yaml`*:
  ```
  logger:
  default: info
  logs:
    custom_components.pyscript.domain_group_by_area: debug
  ```

## Configuration &  Usage
### Initial Configuration
- You have to create an automation for each domain (e.g. light) which should result as a dynamic group entity.
```
  alias: Create area_all_lights group per area on HA startup
trigger:
  - platform: homeassistant
    event: start
action:
  - service: pyscript.domain_group_by_area
    data:
      domain: light
```
- After creating the automation, restart your HA instance or manually execute it.
- If you add new devices of the desired domain to your hass instance, restart your HA instance or
  manually execute it.

### Advances configuration
 - You can define *entity_blacklist* to add specific domain entities to ignore them.
 - You can define *area_whitelist* to limit the considered areas for the group creation.
 - If you want an overall group for all domain entities (except the blacklisted ones) you can add *all* as another option.

 Example config:
```
  alias: Create area_all_lights group per area on HA startup
trigger:
  - platform: homeassistant
    event: start
action:
  - service: pyscript.domain_group_by_area
    data:
      domain: light
      entity_blacklist:
        - light.hmip_bsm_balkonzimmerlicht
        - light.schlaf_shelly1_fenster1
      area_whitelist:
        - buro
        - schlafzimmer
        - flur_unten
      all: true
```

### Update
- Just copy the new `domain_group_by_area.py` to `config/pyscript/domain_group_by_area.py`

### Deactivation
- Go to your autmation and deactivate or delete it.

### Deletion
- Go to your HA instance config dir and delete `config/pyscript/domain_group_by_area.py` or the `config/pyscript` folder (caution!).
