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

End Sub
