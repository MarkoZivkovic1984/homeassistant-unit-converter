from pint import UnitRegistry

ureg = UnitRegistry(autoconvert_offset_to_baseunit=True)

# Map localized unit names to pint units
merne_Kategorije = {
    "Stopa": "ft",
    "Inc": "in",
    "Yard": "yd",
    "Milja": "mi",
    "Nauticka milja": "nmi",
    "Metar": "m",
    "Kilometar": "km",
    "Milimetar": "mm",
    "Centimetar": "cm",
    "Unca": "oz",
    "Funta": "lb",
    "Kilogram": "kg",
    "Gram": "g",
    "Miligram": "mg",
    "Celzijus": "degC",
    "Farenhajt": "degF",
}

@service
def unit_converter(value=None, from_unit=None, to_unit=None):
    raw_value = state.get("input_number.convert_value_2")
    log.info(f"RAW HA input_number value: {raw_value!r}")
    try:
        if value is None:
            value = float(state.get('input_number.convert_value_2'))
    except:
        log.error("Ubaci kolicinu (invalid number).")
        state.set("sensor.unit_converter_internal", "error")
        return

    if not from_unit:
        from_unit = state.get("input_select.convert_from_unit")
    if not to_unit:
        to_unit = state.get("input_select.convert_to_unit")
    if not from_unit or not to_unit:
        log.error("Ubacite merne jedinice.")
        state.set("sensor.unit_converter_internal", "error")
        return

    # Conversion
    try:
        a = ureg.parse_units(merne_Kategorije[from_unit])
        b = ureg.parse_units(merne_Kategorije[to_unit])
        result = (value * a).to(b)

        log.info(f"{value} {from_unit} = {result:.2f} {to_unit}")
        # Set virtual sensor
        state.set("sensor.unit_converter_internal", f"{result:.2f}")

    except Exception as e:
        for _ in str(e):
            if "Cannot convert from" in str(e):
                _ = "Pogresne merne jedinice."
                log.error("Pogresne merne jedinice.")
            elif 'could not converte string to float' in str(e):
                _ = 'Ubaci Kolicinu'
            elif "''" in str(e):
                _ = 'Ubacite Merne Jedinice'
            else:
                log.error(f"Greska: {e}")
                _ = e
            state.set("sensor.unit_converter_internal", _)
