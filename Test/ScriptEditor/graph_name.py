binding.addGraph("", "graph", 867.0, 218.0)
binding_exec = binding.binding.getExec()
print binding_exec.getNodeName(0)
binding.editNode("", "graph", "newGraph", "{}", "{\n  \"uiTooltip\" : \"\",\n  \"uiDocUrl\" : \"\",\n  \"uiNodeColor\" : \"{\\n  \\\"r\\\" : 90,\\n  \\\"g\\\" : 37,\\n  \\\"b\\\" : 143\\n  }\",\n  \"uiTextColor\" : \"{\\n  \\\"r\\\" : 255,\\n  \\\"g\\\" : 213,\\n  \\\"b\\\" : 0\\n  }\",\n  \"uiHeaderColor\" : \"\"\n  }")
print binding_exec.getNodeName(0)