Sub LoadIndexList ()
    Dim thisSht As Worksheet
    Dim sheetName As String
    Dim typeName as String
    Dim outputHead As String
    Dim code As String    

    sheet_name = "IndexData"
    Set thisSht = Sheets(sheet_name)

    typeName = thisSht.Range("C4").Value
    outputHead = thisSht.Range("C5").Value

    code = "import load_index;"
    code = code + "load_index.load_index(sheet_name = '" & sheet_name & "', "
    code = code + "typeName = '" & typeName & "', "
    code = code + "outputHead = '" & outputHead & "')"

    RunPython code
End Sub

Sub LoadIndexPdf ()
    Dim thisSht As Worksheet
    Dim sheetName As String
    Dim codes as String
    Dim outputHead As String
    Dim code As String    

    sheet_name = "IndexData"
    Set thisSht = Sheets(sheet_name)

    codes = thisSht.Range("K4").Value

    outputHead = thisSht.Range("K5").Value

    code = "import load_index;"
    code = code + "load_index.load_index_pdf(sheet_name = '" & sheet_name & "', "
    code = code + "codes = '" & codes & "', "
    code = code + "outputHead = '" & outputHead & "')"

    RunPython code
End Sub

Sub LoadKrxIndexList()
    Dim thisSht As Worksheet
    Dim sheetName As String
    Dim outputHead As String
    Dim dt as String
    Dim code As String

    sheet_name = "IndexData"
    Set thisSht = Sheets(sheet_name)

    outputHead = thisSht.Range("C4").Value
    dt = thisSht.Range("C5").Value

    code = "import krx_index;"
    code = code + "krx_index.load_krx_index_list(sheet_name = '" & sheet_name & "', "
    code = code + "date = '" & dt & "', "
    code = code + "output_head = '" & outputHead & "')"

    RunPython code
End Sub

Sub LoadKrxIndexPdf()
    Dim thisSht As Worksheet
    Dim sheetName As String
    Dim outputHead As String
    Dim dt as String
    Dim code As String

    sheet_name = "IndexData"
    Set thisSht = Sheets(sheet_name)

    outputHead = thisSht.Range("K4").Value
    dt = thisSht.Range("K5").Value

    code = "import krx_index;"
    code = code + "krx_index.load_krx_index_pdf(sheet_name = '" & sheet_name & "', "
    code = code + "codes = '" & codes & "', "
    code = code + "date = '" & dt & "', "
    code = code + "output_head = '" & outputHead & "')"
    
    RunPython code
End Sub

