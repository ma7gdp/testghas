import ldap

user_filter = input("Enter LDAP filter: ")
conn = ldap.initialize('ldap://example.com')
conn.search_s('dc=example,dc=com', ldap.SCOPE_SUBTREE, user_filter)
