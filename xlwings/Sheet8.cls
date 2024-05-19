Sub RankList()
    Dim code As String
    
    code = "from Infomax import stock_list;stock_list.rank_list("
    code = code + "sheet_name = 'List', "
    code = code + "output_range = 'G4:U2000', "
    code = code + "config_range = 'RankConfig')"
    
    Debug.Print (code)
    
    RunPython (code)
End Sub

