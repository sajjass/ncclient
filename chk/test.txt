filterData = '''<if:interfaces xmlns:if="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                    <if:interface>
                        <if:name>0/1</if:name>
                            <if:description/>
                    </if:interface>
                </if:interfaces>'''
configData = '''<nc:config xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
                        <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                             <interface>
                                 <name>0/1</name>
                                       <description nc:operation="%s">%s</description>
                             </interface>
                         </interfaces>
                     </nc:config>'''

