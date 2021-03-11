import subprocess
import ipaddress

from config.operations.params import TRACEROUTE_PARAMS, GENERAL_PARAMS, PING_PARAMS, DNS_PARAMS


class ParamsParser:
    def parse_params(self, params, valid_params):
        command = ""

        for cmd in params:
            if cmd in valid_params:
                manager = valid_params[cmd]

                manager.validate(params[cmd])

                command += manager.parse_command(params[cmd]) + " "

        return command.rstrip()

    def parse_traceroute(self, params):
        params = self.resolve_domain_names(params)
        general_cmd = self.parse_params(params, GENERAL_PARAMS).split(' ')
        sub_cmd = ["trace " + self.parse_params(params, TRACEROUTE_PARAMS)]

        return sub_cmd + general_cmd

    def parse_ping(self, params):
        params = self.resolve_domain_names(params)
        general_cmd = self.parse_params(params, GENERAL_PARAMS).split(' ')
        sub_cmd = ["ping " + self.parse_params(params, PING_PARAMS)]

        return sub_cmd + general_cmd

    def parse_dns(self, params):
        general_cmd = self.parse_params(params, DNS_PARAMS).split(' ')
        return general_cmd

    def resolve_domain_names(self, params):
        if "fqdns" not in params:
            return params
        dig_cmd = ["dig", "+short"] + params["fqdns"]
        dig_proc = subprocess.run(dig_cmd, stdout=subprocess.PIPE)
        dig_output = dig_proc.stdout.decode("utf-8")
        output_lines = dig_output.split('\n')
        ips = []
        for line in output_lines:
            try:
                ipaddress.ip_address(line)
                ips.append(line.strip())
            except ValueError:
                continue
        if "ips" not in params:
            params["ips"] = ips
        else:
            params["ips"] = params["ips"] + ips
        del params["fqdns"]
        return params
