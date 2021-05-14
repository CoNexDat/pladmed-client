## Pladmed client

To run this client: make start
To see logs: make logs
To run and see logs: make debug
To stop the client: make stop

## Configuration

Configuration values are provided via an [env file](https://docs.docker.com/compose/env-file/) called
`config` at the repository root level. Keys and sample values are specified in `config.example`.

Next, an explanation of each key, all of which are **mandatory**.

* **TOKEN**: This is the client's security token. It identifies this client as a probe in the pladmed platform. It's used for authenticating against pladmed-backend. To obtain this token, the user must register in the system, log in and register a new probe. Upon probe registration, the probe token is granted by pladmed-backend.

* **NTP_SERVER**: The [NTP protocol](http://www.ntp.org/) is used to synchronize the client's clock once a day. Since the client runs inside a Docker container, which in turn runs inside a host operating system, to avoid being invasive, the host's clock is not changed. Instead, the Docker container is programmatically "tricked" into seeing the NTP-synchronized time, and the host's clock is left intact. With this context in mind, this key contains a url which references the NTP server which will be used to determine the time. Following the [NTP FAQ's advice on scalability](http://www.ntp.org/ntpfaq/NTP-s-config-adv.htm#AEN3101), this URL should point to pladmed-backend, which runs an NTP server itself. For testing purposes, any [public NTP server](https://www.ntppool.org/en/use.html) will do.

* **UPLOAD_RATE**: Since the client is meant to use limited resources and avoid hogging the host's resources, its network bandwidth is limited. This value is used to limit the data rate for the channel between this probe and the backend. The main consumption in this channel is associated to uploading measurement results from the probe to the server. The expected format is xKbps, where xx is an integer number. Keep in mind that the units are Kilobits per second, not Kilobytes.

* **OPERATIONS_RATE**: Similarly to UPLOAD_RATE, this value limits the combined data rate of the channels between the probe and the arbitrary network hosts it communicates with when performing measuring operations. Heuristically, this represents 62% of the probe's traffic, with the remaining 38% left for uploading results to the server, but your mileage might vary, so these values are left open for tinkering.

* **BACKEND_IP**: Public IPv4 IP address where pladmed-backend runs. Necessary for the probe to communicate with it in order to receive measurement requests, and upload results.

* **BACKEND_PORT**: TCP port where pladmed-backend exposes its service. Together with BACKEND_IP, they locate pladmed-backend in the probe context.

* **TIME_SYNC_PORT, FINISH_OPERATION_PORT, FINISH_TASK_PORT**: These are TCP ports used internally by the probe for inter process communication. Since the probe runs inside a Docker container, there is no possible port collision with the hosts, since these ports are not mapped to ports outside the container. The only thing to be aware of, is that these three have all different values, and don't collide with any well known service port inside the container. The example values should be good enough here.

## Design documentation

* [Packages diagram](doc/packages-diagram.md)

* [Class diagram](doc/class-diagram.md)

* [Scheduling sequence diagram](doc/scheduling.md)

## License
All releases of PlaDMed are licensed under the GPL v2.
