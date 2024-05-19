Sub LoadEtfData()
    Dim code As String
    Dim sheet_name As String
    Dim file_name As String
    Dim etf_info_file_name As String
    Dim output_range As String
    
    sheet_name = "LoadEtfData"
    file_name = Worksheets(sheet_name).Range("C3").Value
    etf_info_file_name = Worksheets(sheet_name).Range("C4").Value
    
    output_range = "G3:M5000"
    
    code = "import load_etf_info;load_etf_info.load_etf_info("
    code = code + "sheet_name = '" + sheet_name + "', "
    code = code + "file_name = '" + file_name + "', "
    code = code + "etf_info_file_name = '" + etf_info_file_name + "', "
    code = code + "output_range = '" + output_range + "')"
    
    RunPython code
End Sub
