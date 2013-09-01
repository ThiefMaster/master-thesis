<%inherit file="Footer.CERN.tpl" />
<%block name="footer">
% if showSocial:
    <%include file="SocialIcons.tpl" args="dark=dark,url=shortURL"/>
% endif
    ${parent.footer()}
</%block>
