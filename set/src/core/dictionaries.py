#!/usr/bin/env python

""" Python lists used for quick conversion of user input
    to strings used by the toolkit """
    
def encoder_type(encode):
    """ 
    Takes the value sent from the user encoding menu and returns
    the actual value to be used. """

    return {
            '0':"",
            '1':"avoid_utf8_tolower",
            '2':"shikata_ga_nai",
            '3':"alpha_mixed",
            '4':"alpha_upper",
            '5':"call4_dword_xor",
            '6':"countdown",
            '7':"fnstenv_mov",
            '8':"jmp_call_additive",
            '9':"nonalpha",
            '10':"nonupper",
            '11':"unicode_mixed",
            '12':"unicode_upper",
            '13':"alpha2",
            '14':"",
            '15':"MULTIENCODE",
            '16':"BACKDOOR",
            }.get(encode,"ERROR")


def ms_module(exploit):
    
    """
    Receives the input given by the user from gen_payload.py """
    
    return {
            '1':"multi/browser/java_rhino\nset target 1",
            '2':"windows/browser/ms11_050_mshtml_cobjectelement",
            '3':"windows/browser/adobe_flashplayer_flash10o",
            '4':"windows/browser/cisco_anyconnect_exec",
            '5':"windows/browser/ms11_003_ie_css_import",
            '6':"windows/browser/wmi_admintools",
            '7':"windows/browser/ms10_090_ie_css_clip",
            '8':"windows/browser/java_codebase_trust",
            '9':"windows/browser/java_docbase_bof",
            '10':"windows/browser/webdav_dll_hijacker",
            '11':"windows/browser/adobe_flashplayer_avm",
            '12':"windows/browser/adobe_shockwave_rcsl_corruption",
            '13':"windows/browser/adobe_cooltype_sing",
            '14':"windows/browser/apple_quicktime_marshaled_punk",
            '15':"windows/browser/ms10_042_helpctr_xss_cmd_exec",
            '16':"windows/browser/ms10_018_ie_behaviors",
            '17':"windows/browser/ms10_002_aurora",
            '18':"windows/browser/ms10_018_ie_tabular_activex",
            '19':"windows/browser/ms09_002_memory_corruption",
            '20':"windows/browser/ms09_072_style_object",
            '21':"windows/browser/ie_iscomponentinstalled",
            '22':"windows/browser/ms08_078_xml_corruption",
            '23':"windows/browser/ie_unsafe_scripting",
            '24':"multi/browser/firefox_escape_retval",
            '25':"windows/browser/mozilla_mchannel",
            '26':"auxiliary/server/browser_autopwn",
           }.get(exploit,"ERROR")
           

# called from gen_payload.py
# uses payload_menu_2
def ms_payload(payload):
    
    """
    Receives the input given by the user from create_payload.py 
    and create_payloads.py """
    
    return {
            '1':"windows/shell_reverse_tcp",
            '2':"windows/meterpreter/reverse_tcp",
            '3':"windows/vncinject/reverse_tcp",
            '4':"windows/shell_bind_tcp",
            '5':"windows/x64/shell_bind_tcp",
            '6':"windows/x64/shell_reverse_tcp",
            '7':"windows/x64/meterpreter/reverse_tcp",
            '8':"windows/meterpreter/reverse_tcp_allports",
            '9':"windows/meterpreter/reverse_https",
            '10':"windows/meterpreter/reverse_tcp_dns",
            '11':"windows/download_exec",
            }.get(payload,"ERROR")
            
# called from create_payloads.py

def ms_payload_2(payload):
    
    """
    Receives the input given by the user from create_payloadS.py """
    
    return {
            '1':"windows/shell_reverse_tcp",
            '2':"windows/meterpreter/reverse_tcp",
            '3':"windows/vncinject/reverse_tcp",
            '4':"windows/shell_bind_tcp",
            '5':"windows/x64/shell_bind_tcp",
            '6':"windows/x64/shell_reverse_tcp",
            '7':"windows/x64/meterpreter/reverse_tcp",
            '8':"windows/meterpreter/reverse_tcp_allports",
            '9':"windows/meterpreter/reverse_https",
            '10':"windows/meterpreter/reverse_tcp_dns",
            '11':"set/reverse_shell",
            '12':"set/reverse_shell",
            '13':"shellcode/alphanum",
            }.get(payload,"ERROR")
            
def ms_payload_3(payload):
    
    """
    Receives the input given by the user from create_payloadS.py """
    
    return {
            '1':"windows/shell_reverse_tcp",
            '2':"windows/meterpreter/reverse_tcp",
            '3':"windows/vncinject/reverse_tcp",
            '4':"windows/x64/shell_reverse_tcp",
            '5':"windows/x64/meterpreter/reverse_tcp",
            '6':"windows/x64/shell_bind_tcp",
            '7':"windows/meterpreter/reverse_https",
            }.get(payload,"ERROR")


# uses create_payloads_menu
def ms_attacks(exploit):
    
    """
    Receives the input given by the user from create_payload.py """
    
    return {
            '1':"dll_hijacking",
            '2':"unc_embed",
            '3':"exploit/windows/fileformat/ms11_006_createsizeddibsection",
            '4':"exploit/windows/fileformat/ms10_087_rtf_pfragments_bof",
            '5':"exploit/windows/fileformat/adobe_flashplayer_button",
            '6':"exploit/windows/fileformat/adobe_cooltype_sing",
            '7':"exploit/windows/fileformat/adobe_flashplayer_newfunction",
            '8':"exploit/windows/fileformat/adobe_collectemailinfo",
            '9':"exploit/windows/fileformat/adobe_geticon",
            '10':"exploit/windows/fileformat/adobe_jbig2decode",
            '11':"exploit/windows/fileformat/adobe_pdf_embedded_exe",
            '12':"exploit/windows/fileformat/adobe_utilprintf",
            '13':"custom/exe/to/vba/payload",
            '14':"exploit/windows/fileformat/adobe_u3d_meshdecl",
            '15':'exploit/windows/fileformat/adobe_pdf_embedded_exe_nojs',
            '16':"exploit/windows/fileformat/foxit_title_bof",
            '17':"exploit/windows/fileformat/apple_quicktime_pnsize",
            '18':"exploit/windows/fileformat/nuance_pdf_launch_overflow",
            '19':"exploit/windows/fileformat/adobe_reader_u3d",
            }.get(exploit,"ERROR")
            
def teensy_config(choice):
    
    """
    Receives the input given by the user from set.py """
    
    return {
            '1':"powershell_down.pde",
            '2':"wscript.pde",
            '3':"powershell_reverse.pde",
            '4':"beef.pde",
            '5':"java_applet.pde",
            '6':"gnome_wget.pde"
            }.get(choice,"ERROR")
            
def webattack_vector(attack_vector):
    
    """
    Receives the input given by the user from set.py """
    
    return {
            '1':"java",
            '2':"browser",
            '3':"harvester",
            '4':"tabnapping",
            '5':"mlitme",
            '6':"webjacking",
            '7':"multiattack"
            }.get(attack_vector,"ERROR")
            

def category(category):
    """ 
    Takes the value sent from the user encoding menu and returns
    the actual value to be used. """

    return {
            '0':"0",
            '1':"phishing",
            '2':"webattack",
            '3':"infectious",
            '4':"payloads",
            '5':"mailer",
            '6':"arduino",
            '7':"sms",
            '8':"wireless",
            '9':"modules",
            '10':"cloner",
            '11':"harvester",
            '12':"tabnapping",
            '13':"teensy",
            '14':"binary2teensy",
            '15':"dll_hijacking",
            '16':"multiattack",
            '17':"java_applet",
            '18':"encoding",
            '19':"fasttrack",
            '20':"autopwn",
            '21':"mssql",
            '22':"scan",
            '23':"direct",
            '24':"exploits",
            '25':"active_target",
            '26':"shell",
            '27':"set",
            '28':"teensy2powershell"
           }.get(category,"ERROR")

