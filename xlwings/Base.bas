Attribute VB_Name = "Base"
Option Explicit

Sub LoadInfomaxETFBaseData()
    Dim ws As Worksheet
    Dim sheet_name As String
    Dim parameter_date As String
    Dim python_code As String
    Dim file_name As String
    Dim output_head As String

    sheet_name = "BaseData"
    Set ws = ThisWorkbook.Sheets(sheet_name)

    parameter_date = ws.Range("C4").Value
    file_name = ws.Range("C5").Value
    output_head = ws.Range("C6").Value
    ' erase the 1000 rows and 30 columns from output_head
    ws.Range(output_head).Resize(1000, 30).ClearContents

    python_code = "import base_data;"
    python_code = python_code & "base_data.load_infomax_etf_base_data("
    python_code = python_code & "sheet_name='" & sheet_name & "',"
    python_code = python_code & "parameter_date='" & parameter_date & "',"
    python_code = python_code & "file_name='" & file_name & "',"
    python_code = python_code & "output_head='" & output_head & "')"

    RunPython python_code
End Sub

Sub SaveInjfomaxETFBaseData()
    Dim ws As Worksheet
    Dim sheet_name As String
    Dim retrieval_date As String
    Dim parameter_date As String
    Dim python_code As String
    Dim file_name As String

    sheet_name = "BaseData"
    Set ws = ThisWorkbook.Sheets(sheet_name)

    retrieval_date = ws.Range("C3").Value
    parameter_date = ws.Range("C4").Value
    file_name = ws.Range("C5").Value

    python_code = "import base_data;"
    python_code = python_code & "base_data.save_infomax_etf_base_data("
    python_code = python_code & "retrieval_date='" & retrieval_date & "',"
    python_code = python_code & "parameter_date='" & parameter_date & "',"
    python_code = python_code & "file_name='" & file_name & "')"

    RunPython python_code
End Sub

Sub LoadList()
    Dim ws As Worksheet
    Dim sheet_name As String
    Dim python_code As String
    Dim dt As String
    Dim market As String
    Dim type_name As String
    Dim rank As String
    Dim start_date As String
    Dim end_date As String
    Dim investor As String
    Dim num_code As String
    Dim num_page As String
    Dim base_file_date As String
    Dim file_name As String
    Dim output_head As String

    sheet_name = "List"
    Set ws = ThisWorkbook.Sheets(sheet_name)

    dt = ws.Range("C5").Value
    market = ws.Range("C6").Value
    type_name = ws.Range("C7").Value
    rank = ws.Range("C8").Value
    start_date = ws.Range("C9").Value
    end_date = ws.Range("C10").Value
    investor = ws.Range("C11").Value
    num_code = ws.Range("C12").Value
    num_page = ws.Range("C13").Value
    base_file_date = ws.Range("C14").Value
    file_name = ws.Range("C15").Value
    output_head = ws.Range("C16").Value

    If market = "��ü" Then
        market = ""
    ElseIf market = "�ŷ���" Then
        market = "1"
    ElseIf market = "�ŷ��� ��Ÿ" Then
        market = "2"
    ElseIf market = "KRX" Then
        market = "5"
    ElseIf market = "�ڽ���" Then
        market = "7"
    ElseIf market = "�ڽ��� ��Ÿ" Then
        market = "8"
    End If
    
    If rank = "�ŷ����" Then
        rank = "trading"
    ElseIf rank = "�ð��Ѿ�" Then
        rank = "cap"
    ElseIf rank = "�����" Then
        rank = "rate"
    End If

    python_code = "import infomax_base_data;"
    python_code = python_code & "infomax_base_data.load_list("
    python_code = python_code & "sheet_name='" & sheet_name & "',"
    python_code = python_code & "date='" & dt & "',"
    python_code = python_code & "market='" & market & "',"
    python_code = python_code & "type_name='" & type_name & "',"
    python_code = python_code & "rank='" & rank & "',"
    python_code = python_code & "start_date='" & start_date & "',"
    python_code = python_code & "end_date='" & end_date & "',"
    python_code = python_code & "investor='" & investor & "',"
    python_code = python_code & "num_code=" & num_code & ","
    python_code = python_code & "num_page=" & num_page & ","
    python_code = python_code & "base_file_date='" & base_file_date & "',"
    python_code = python_code & "file_name='" & file_name & "',"
    python_code = python_code & "output_head='" & output_head & "')"

    RunPython python_code
End Sub
