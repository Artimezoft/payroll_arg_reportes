

def process_reg4(txt_info_line: str, no_rem_os: float = 0.0, id_liquidaciones_anteriores: list = []) -> str:
    resp = ''
    cuil = get_value_from_txt(txt_info_line, 'CUIL')
    reg4_qs = OrdenRegistro.objects.filter(tiporegistro__order=4)

    mod_cont = int(get_value_from_txt(txt_info_line, 'Código de Modalidad de Contratación'))
    rem2 = amount_txt_to_integer(get_value_from_txt(txt_info_line, 'Remuneración Imponible 2'))
    rem4 = amount_txt_to_integer(get_value_from_txt(txt_info_line, 'Remuneración Imponible 4'))
    rem8 = amount_txt_to_integer(get_value_from_txt(txt_info_line, 'Rem.Dec.788/05 - Rem Impon. 8'))
    # rem9 = amount_txt_to_integer(get_value_from_txt(txt_info_line, 'Remuneración Imponible 9'))
    rem10 = amount_txt_to_integer(get_value_from_txt(txt_info_line, 'Remuneración Imponible 2'))
    detr = amount_txt_to_integer(get_value_from_txt(txt_info_line, 'Importe a detraer Ley 27430'))

    # Porque da error SR consecutivas iguales
    sr1 = get_value_from_txt(txt_info_line, 'Situación de Revista 1')
    sr2 = get_value_from_txt(txt_info_line, 'Situación de Revista 2')
    sr3 = get_value_from_txt(txt_info_line, 'Situación de Revista 3')

    tmp_sr2 = '  ' if sr1 == sr2 else sr2
    sr3 = '  ' if sr2 == sr3 else sr3
    sr2 = tmp_sr2

    no_rem_os_liq_anteriores = 0
    for id_liq in id_liquidaciones_anteriores:
        no_rem_os_liq_anteriores += get_nros_from_liq(cuil=cuil, id_liq=id_liq)

    for reg in reg4_qs:
        if reg.formatof931:
            # Si está lo vinculo puliendo formato
            multip = 100 if reg.formatof931.name in MULTIP_100 else 1
            tmp_linea = sync_format(get_value_from_txt(txt_info_line, reg.formatof931.name), reg.long, reg.type, multip)
            if reg.formatof931.name == 'Cónyuge' or reg.formatof931.name == 'Trabajador Convencionado 0-No 1-Si' or\
                    reg.formatof931.name == 'Seguro Colectivo de Vida Obligatorio' or\
                    reg.formatof931.name == 'Marca de Corresponde Reducción':

                tmp_linea = tmp_linea.replace('T', '1').replace('F', '0')

            elif reg.formatof931.name == 'Situación de Revista 2':
                tmp_linea = sr2

            elif reg.formatof931.name == 'Situación de Revista 3':
                tmp_linea = sr3

            resp += tmp_linea

        else:
            # Si no está, cargo los casos específicos y dejo vacío el resto (0 números y " " texto)
            if reg.name == 'Identificación del tipo de registro':
                resp += '04'
            elif reg.name == 'Base imponible 10':
                rem10 = rem10 - detr

                if detr == 0 or mod_cont in NOT_SIJP:
                    rem10 = 0

                resp += str(rem10).zfill(15)
            elif reg.name == 'Base para el cálculo diferencial de aporte de obra social y FSR (1)':
                # Valido R4
                # R4 = Rem + NR OS y Sind + Ap.Ad.OS
                # Ap.Ad.OS = R4 - Rem - NR OS y Sind
                resta = rem2 + no_rem_os + no_rem_os_liq_anteriores
                aa_os = max(0, rem4 - resta)
                resp += str(aa_os).zfill(15)

            elif reg.name == 'Base para el cálculo diferencial de contribuciones de obra social y FSR (1)':
                # Valido R8
                # R8 = Rem + NR OS y Sind + Ct.Ad.OS
                # Ct.Ad.OS = R8 - Rem - NR OS y Sind
                resta = rem2 + no_rem_os + no_rem_os_liq_anteriores
                ca_os = max(0, rem8 - resta)
                resp += str(ca_os).zfill(15)

            else:
                resp += "0" * reg.long

    return resp
