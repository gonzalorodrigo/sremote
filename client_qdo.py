from xml_marshaller import xml_marshaller


input_dic = {'first':'value1', 'second':'value2'}
serialized_dic = xml_marshaller.dumps(input_dic)

#call_dic = {'method': 'remote_method', 'args':[input_dic]}
call_dic = {'method': 'qlist', 'args':[]}

print xml_marshaller.dumps(call_dic)
