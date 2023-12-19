# ha_domain_group_by_area

DESCRIPTION MISSING

If you like my work, you can support me here:\
<a href="https://www.buymeacoffee.com/chillje" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>

## Feature list
:white_check_mark: Works with different domains (such as "light", "switch", ..)\
:white_check_mark: Automatic creation for all created areas\
:white_check_mark: Blacklist for single entities\
:white_check_mark: Whitelist for single areas


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
- You have to create for each domain (e.g. light) which should be exist a group by area a new automation
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
- After creating the automation, restart your HA instance or manually execute it
- If you add new devices of the desired domain to your hass instance, restart your HA instance or
  manually execute it again.

### Advances configuration
 - You can define *entity_black_list* to add specific domain entities to ignore them
 - You can define *area_whitelist* to limit the considered areas for the group creation.

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
      entity_black_list:
        - light.hmip_bsm_balkonzimmerlicht
        - light.schlaf_shelly1_fenster1
      area_whitelist:
        - buro
        - schlafzimmer
        - flur_unten
```

### Update
- Just copy the new `domain_group_by_area.py` to `config/pyscript/domain_group_by_area.py`$

### Deactivation
- To deactivate the script, go to your autmation an deactivate or delete it.

### Deletion
- Go to your HA config dir and delete `config/pyscript/domain_group_by_area.py` or the `config/pyscript` folder (caution!).
