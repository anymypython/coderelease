from django.test import TestCase

# Create your tests here.

a = {'ok': {'10.0.0.6': {'nginx_down': {'msg': '', 'invocation': {
    'module_args': {'directory_mode': None, 'force': None, 'encoding': 'utf-8', 'replace': '#\\1',
                    'path': '/etc/nginx/nginx.conf', 'owner': None, 'follow': False, 'before': None, 'group': None,
                    'unsafe_writes': None, 'remote_src': None, 'setype': None, 'content': None, 'serole': None,
                    'selevel': None, 'after': None, 'regexp': '(10.0.0.6.*)', 'validate': None, 'src': None,
                    'seuser': None, 'delimiter': None, 'mode': None, 'attributes': None, 'backup': False}},
                                        'changed': False, '_ansible_parsed': True, '_ansible_no_log': False},
                         'nginx_reload': {'status': {
                             'ExecStart': '{ path=/usr/sbin/nginx ; argv[]=/usr/sbin/nginx ; ignore_errors=no ; start_time=[Sun 2019-03-31 19:58:39 CST] ; stop_time=[Sun 2019-03-31 19:58:40 CST] ; pid=1645 ; code=exited ; status=0 }',
                             'TimeoutStopUSec': '5s', 'ControlGroup': '/system.slice/nginx.service',
                             'RuntimeDirectoryMode': '0755', 'GuessMainPID': 'yes', 'ExecMainCode': '0',
                             'ExecStartPre': '{ path=/usr/sbin/nginx ; argv[]=/usr/sbin/nginx -t ; ignore_errors=no ; start_time=[Sun 2019-03-31 19:58:39 CST] ; stop_time=[Sun 2019-03-31 19:58:39 CST] ; pid=1643 ; code=exited ; status=0 }',
                             'UnitFileState': 'disabled', 'ExecMainPID': '1647', 'LimitSIGPENDING': '3802',
                             'FileDescriptorStoreMax': '0', 'LoadState': 'loaded', 'ProtectHome': 'no',
                             'TTYVTDisallocate': 'no', 'StartLimitInterval': '10000000',
                             'WatchdogTimestampMonotonic': '0', 'LimitSTACK': '18446744073709551615',
                             'ActiveEnterTimestampMonotonic': '265644982', 'AllowIsolate': 'no',
                             'IgnoreOnSnapshot': 'no', 'StartLimitAction': 'none', 'CPUSchedulingPriority': '0',
                             'KillSignal': '3', 'LimitFSIZE': '18446744073709551615', 'IgnoreOnIsolate': 'no',
                             'LimitCPU': '18446744073709551615', 'AssertTimestamp': 'Sun 2019-03-31 19:58:39 CST',
                             'ActiveEnterTimestamp': 'Sun 2019-03-31 19:58:40 CST',
                             'MemoryLimit': '18446744073709551615', 'TTYReset': 'no', 'CanStart': 'yes',
                             'JobTimeoutAction': 'none', 'NoNewPrivileges': 'no', 'Before': 'shutdown.target',
                             'LimitAS': '18446744073709551615', 'RootDirectoryStartOnly': 'no',
                             'InactiveExitTimestampMonotonic': '265296516', 'SendSIGHUP': 'no',
                             'TimeoutStartUSec': '1min 30s', 'Type': 'forking', 'SyslogPriority': '30',
                             'SameProcessGroup': 'no', 'LimitNPROC': '3802', 'UMask': '0022', 'NonBlocking': 'no',
                             'DevicePolicy': 'auto', 'ExecMainStartTimestamp': 'Sun 2019-03-31 19:58:40 CST',
                             'CapabilityBoundingSet': '18446744073709551615', 'PIDFile': '/run/nginx.pid',
                             'OOMScoreAdjust': '0', 'StartLimitBurst': '5', 'RefuseManualStart': 'no',
                             'KillMode': 'process', 'SyslogLevelPrefix': 'yes', 'LimitRSS': '18446744073709551615',
                             'LimitRTPRIO': '0', 'Delegate': 'no',
                             'ExecReload': '{ path=/bin/kill ; argv[]=/bin/kill -s HUP $MAINPID ; ignore_errors=no ; start_time=[Sun 2019-03-31 20:00:59 CST] ; stop_time=[Sun 2019-03-31 20:00:59 CST] ; pid=2434 ; code=exited ; status=0 }',
                             'TasksCurrent': '18446744073709551615', 'LimitCORE': '18446744073709551615',
                             'JobTimeoutUSec': '0', 'TimerSlackNSec': '50000', 'SubState': 'running',
                             'CPUSchedulingResetOnFork': 'no', 'Result': 'success', 'CPUShares': '18446744073709551615',
                             'ConditionResult': 'yes', 'ConditionTimestampMonotonic': '265289229', 'MainPID': '1647',
                             'StartupBlockIOWeight': '18446744073709551615',
                             'InactiveExitTimestamp': 'Sun 2019-03-31 19:58:39 CST',
                             'FragmentPath': '/usr/lib/systemd/system/nginx.service',
                             'StartupCPUShares': '18446744073709551615', 'WatchdogUSec': '0', 'ActiveState': 'active',
                             'Nice': '0', 'LimitDATA': '18446744073709551615', 'UnitFilePreset': 'disabled',
                             'MemoryCurrent': '18446744073709551615', 'LimitRTTIME': '18446744073709551615',
                             'SecureBits': '0', 'RestartUSec': '100ms',
                             'ConditionTimestamp': 'Sun 2019-03-31 19:58:39 CST', 'CPUAccounting': 'no',
                             'RemainAfterExit': 'no', 'RequiresMountsFor': '/var/tmp', 'PrivateNetwork': 'no',
                             'Restart': 'no', 'CPUSchedulingPolicy': '0', 'LimitNOFILE': '4096', 'SendSIGKILL': 'yes',
                             'StatusErrno': '0', 'RefuseManualStop': 'no', 'SystemCallErrorNumber': '0',
                             'TasksAccounting': 'no', 'NeedDaemonReload': 'no', 'TTYVHangup': 'no',
                             'StandardInput': 'null', 'AssertTimestampMonotonic': '265289230',
                             'DefaultDependencies': 'yes', 'Requires': 'basic.target -.mount',
                             'TasksMax': '18446744073709551615', 'CPUQuotaPerSecUSec': 'infinity',
                             'ExecMainStatus': '0', 'LimitMEMLOCK': '65536', 'StopWhenUnneeded': 'no',
                             'LimitMSGQUEUE': '819200', 'AmbientCapabilities': '0', 'Slice': 'system.slice',
                             'ExecMainExitTimestampMonotonic': '0', 'NotifyAccess': 'none',
                             'PermissionsStartOnly': 'no', 'BlockIOAccounting': 'no', 'CanStop': 'yes',
                             'PrivateTmp': 'yes', 'OnFailureJobMode': 'replace', 'AssertResult': 'yes',
                             'LimitLOCKS': '18446744073709551615', 'ExecMainStartTimestampMonotonic': '265644750',
                             'StandardError': 'inherit', 'Wants': 'system.slice',
                             'After': 'tmp.mount -.mount nss-lookup.target systemd-journald.socket remote-fs.target network.target basic.target system.slice',
                             'FailureAction': 'none', 'CanIsolate': 'no', 'Conflicts': 'shutdown.target',
                             'StandardOutput': 'journal', 'MountFlags': '0', 'InactiveEnterTimestampMonotonic': '0',
                             'MemoryAccounting': 'no', 'IgnoreSIGPIPE': 'yes', 'Transient': 'no', 'IOScheduling': '0',
                             'Description': 'The nginx HTTP and reverse proxy server',
                             'ActiveExitTimestampMonotonic': '0', 'CanReload': 'yes', 'ControlPID': '0',
                             'LimitNICE': '0', 'BlockIOWeight': '18446744073709551615', 'Names': 'nginx.service',
                             'ProtectSystem': 'no', 'PrivateDevices': 'no', 'Id': 'nginx.service'}, 'invocation': {
                             'module_args': {'no_block': False, 'force': None, 'name': 'nginx', 'enabled': None,
                                             'daemon_reload': False, 'state': 'reloaded', 'masked': None, 'scope': None,
                                             'user': None}}, 'state': 'started', 'changed': True, 'name': 'nginx',
                             '_ansible_parsed': True, '_ansible_no_log': False}}}, 'failed': {},
     'unreachable': {}, 'skipped': {}}


d = {"a": 1, "b": 2}
print(list(d))
print(dir(type(enumerate(d))))
