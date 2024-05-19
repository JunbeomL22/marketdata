Attribute VB_Name = "Utils"
Option Explicit

Public Function JoinText(arr As Range, joiner As String) As String
    Dim cell As Range
    Dim strArr() As String
    Dim i As Integer

    ReDim strArr(arr.Cells.Count - 1)
    i = 0

    For Each cell In arr
        strArr(i) = cell.Value
        i = i + 1
    Next cell

    JoinText = Join(strArr, joiner)
End Function
