Attribute VB_Name = "EtfAnalysis"
Option Explicit

Public Sub LoadAndGraph()
    Dim ws As Worksheet
    Dim sheetName As String
    Dim outputHead As String
    Dim etfCode As String
    Dim etfName As String
    Dim fromDate As String
    Dim toDate As String
    Dim field1 As String
    Dim field2 As String
    Dim period As String
    Dim valueType As String

    Dim code As String

    sheetName = "EtfAnalysis"
    Set ws = ThisWorkbook.Sheets(sheetName)
    etfCode = ws.Range("C3").Value
    etfName = ws.Range("C4").Value
    fromDate = ws.Range("C5").Value
    toDate = ws.Range("C6").Value
    field1 = ws.Range("C7").Value
    field2 = ws.Range("C8").Value
    period = ws.Range("C9").Value
    valueType = ws.Range("C10").Value
    outputHead = ws.Range("C11").Value

    ' clear the output area 20 columns and 1000 rows from the outputHead
    ws.Range(outputHead).Resize(1000, 20).ClearContents

    code = "import krx_etf_info;"
    code = code & "krx_etf_info.load_and_graph("
    code = code & "sheet_name='" & sheetName & "', "
    code = code & "output_head='" & outputHead & "', "
    code = code & "code='" & etfCode & "', "
    code = code & "name='" & etfName & "', "
    code = code & "fromdate='" & fromDate & "', "
    code = code & "todate='" & toDate & "', "
    code = code & "field1='" & field1 & "', "
    code = code & "field2='" & field2 & "', "
    code = code & "period='" & period & "', "
    code = code & "value_type='" & valueType & "')"

    RunPython code

End Sub
