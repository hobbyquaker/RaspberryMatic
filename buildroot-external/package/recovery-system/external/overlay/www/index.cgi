#!/bin/sh

echo -ne "Content-Type: text/html; charset=iso-8859-1\r\n\r\n"

if [ -f /tmp/.runningFirmwareUpdate ]; then
  echo "Displaying running firmware update output:<br/>"
  echo "==========================================<br/>"

  [ -f /tmp/fwinstall.pid ] && kill $(cat /tmp/fwinstall.pid)
  /usr/bin/tail -F /tmp/fwinstall.log &
  echo $! >/tmp/fwinstall.pid
  wait $!

  echo "<br/>==========================================<br/>"
  echo "FINISHED<br/>"
  exit 0
fi

cat <<EOF
<html>
  <head>
    <meta http-equiv="expires" content="0">
    <title>CCU Recovery System</title>
    <style type="text/css">

      body {
        background-color:#192c6e;
        color:white
      }

      h1 {
        margin-top:1em;
        font-weight: bold;
        padding-top:8px;
      }

      p {
        font-weight: bold;
      }

      .NavButton 	{
        background-color:#ebf1f2;

        /* Safari 4-5, Chrome 1-9 */
        background: -webkit-gradient(linear, 0% 0%, 0% 100%, from(#ffffff), to(#89989b));

        /* Safari 5.1, Chrome 10+ */
        background: -webkit-linear-gradient(top, #ffffff, #89989b);

        /* Firefox 3.6+ */
        background: -moz-linear-gradient(bottom, #89989b, #ffffff);

        /* IE 10 */
        background: -ms-linear-gradient(top, #89989b, #ffffff);
        overflow: auto;

        /* For Internet Explorer 8 */
        -ms-filter: "progid:DXImageTransform.Microsoft.gradient(startColorstr= #d0d0d0, endColorstr=#ffffff)";

        width: 180px;
        text-align: center;
        border: solid 1px;
        cursor: pointer;
        border-radius: 5px;
        font-size: 15px;
        padding-top: 5px;
        padding-bottom: 5px;
      }

    </style>
  </head>
  <body bgcolor="#cccccc" text="#000000">
    <div id="webuilaoder_background">
      <div id="webuilaoder">
        <div id="webuiloader_icon"></div>
        <p><img style="float: left;" src="img/homematic_logo_small.png"/></p>
        <h1>CCU Recovery System</h1>
        <hr noshade size="4" align="left" color="white">
      </div>
    </div>

    <p></p>

    <table>
      <tr>
        <td>
          <form name="frmUpload" action="cgi-bin/firmware_update.cgi" method="post" enctype="multipart/form-data">
            <p>Recovery/Update File<br/>
              <div id='wrapper_'>
                <input type="file" name="Datei" ><br/><br/>
              </div>
              <br/>
              <input class="NavButton" type="submit" value="Start Recovery/Update" >
            </p>
          </form>
        </td>
        <td>
          <form name="bakUpload" action="cgi-bin/restore_backup.cgi" method="post" enctype="multipart/form-data">
            <p>Restore and Backup Configuration<br/>
              <div id='wrapper_'>
                Security Key (optional): <input type="text" id="seckey" name="seckey"><br/>
                Backup File: <input type="file" name="Datei" >
              </div>
              <br/>
              <input class="NavButton" type="submit" value="Restore Backup" >
              <input class="NavButton" type="button" onclick="window.location.href = 'cgi-bin/create_backup.cgi';" value="Create Backup">
            </p>
          </form>
        </td>
      </tr>
    </table>

    <hr noshade size="1" align="left" color="white">
    <input class="NavButton" type="button" onclick="window.location.href = 'cgi-bin/factory_reset.cgi';" value="Factory Reset">

    <input class="NavButton" type="button" onclick="window.location.href = 'cgi-bin/network_reset.cgi';" value="Reset Network Settings">

    <input class="NavButton" type="button" onclick="window.location.href = 'cgi-bin/safemode_boot.cgi';" value="Safe Mode Reboot">

    <input class="NavButton" type="button" onclick="window.location.href = 'cgi-bin/normal_boot.cgi';" value="Normal Reboot">

    <hr noshade size="4" align="left" color="white">
    <p style="font-size:9px; color:lightgrey">
      recoveryfs: $(cat /VERSION | grep "VERSION=" | cut -f2 -d=)<br/>
      bootfs: $(cat /bootfs/VERSION | grep "VERSION=" | cut -f2 -d=)<br/>
      rootfs: $(cat /rootfs/VERSION | grep "VERSION=" | cut -f2 -d=)
    </p>
  </body>
</html>
EOF
