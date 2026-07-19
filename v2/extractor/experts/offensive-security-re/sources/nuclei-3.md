# Nuclei v2 -> v3 Migration Source (nuclei / ProjectDiscovery)

Compiled verbatim from:
- https://github.com/orgs/projectdiscovery/discussions/5208  (How to migrate nuclei templates from old syntax to new)
- https://github.com/projectdiscovery/nuclei/discussions/3648  (v2.9.3 deprecation warnings -> removed in v2.9.5)
- https://projectdiscovery.io/blog/nuclei-v3-featurefusion  (Nuclei v3 announcement, 2023-10-19)
- https://docs.projectdiscovery.io/templates/protocols/flow (v3 flow engine)
- https://docs.projectdiscovery.io/templates/protocols/http/basic-http
- https://docs.projectdiscovery.io/templates/protocols/network (TCP protocol)
- https://docs.projectdiscovery.io/opensource/nuclei/running (CLI flags reference)
- https://docs.projectdiscovery.io/templates/introduction , /templates/faq

======================================================================
## SECTION 1 - Template migration discussion #5208 (old syntax -> new syntax)
======================================================================

Question: How to migrate nuclei templates from the old syntax to the new syntax
(migrating templates from Nuclei v2.8.8 to v3).

Answer (tarunKoyalwar, maintainer):
The primary change involves the protocol identifier. The HTTP protocol block key
must be updated from `requests:` to `http:`. This can easily be automated via `sed`
or any bash match/replace.

  OLD (v2):                      NEW (v3):
    requests:                      http:
      - method: GET                  - method: GET

- Breaking changes for v3 are documented in discussion #3648.
- Nuclei v3 includes deprecation warnings but maintains backward compatibility with
  older syntax, so most templates still function (with warnings).
- Nuclei and Nuclei Templates are treated as a single unified system.
- No LTS versions are provided; users are encouraged to stay current.
- Resolution: the changelog + docs were sufficient to migrate ~2,000 internal templates.

======================================================================
## SECTION 2 - Deprecation-warning discussion #3648 (v2.9.3 -> removal in v2.9.5)
======================================================================

Nuclei v2.9.3 introduced two warning messages:
  - Deprecated path reference warning:
      "Found N templates loaded with deprecated paths, update before v2.9.5 for continued support"
  - Old protocol attribute warning:
      "Found N templates loaded with deprecated protocol syntax, update before v2.9.5 for continued support"

Timeline:
  - v2.9.3: warnings introduced; backward compatibility maintained.
  - v2.9.5: support for older/outdated template formats REMOVED.
Recommended actions:
  - Update: `nuclei -update`
  - Reset config: `nuclei -reset`
Public templates auto-updated via nuclei-templates v9.5.0; custom/private templates
must be updated manually.

======================================================================
## SECTION 3 - Migration guide synthesis (protocol + flag renames, v2 -> v3)
======================================================================

Protocol / template field renames (old v2 -> new v3):
  - `requests:`  ->  `http:`      (HTTP protocol block key)
  - `network:`   ->  `tcp:`       (TCP/network protocol block key)  [v3 docs show the network block starting with `tcp:`]

Execution model:
  - v2 used implicit sequential execution of multiple requests.
  - v3 adds an explicit `flow:` field using JavaScript (ECMAScript 5.1 via goja) to
    orchestrate/conditionally execute requests, e.g. `flow: http(1) && http(2)`.

Command-line flag renames (old -> new):
  - `-fuzz`  ->  `-dast`            (`-fuzz` still loads fuzzing/DAST templates but is Deprecated: use -dast)
  - `-cup` / `-cloud-upload`  ->  `-dashboard`   (DEPRECATED use -dashboard)
  - `-rlm` / `-rate-limit-minute`  ->  DEPRECATED (use `-rl` / `-rate-limit`)
  - `-irr` / `-include-rr`  ->  DEPRECATED (use `-omit-raw`)
  - `-ztls`  ->  Deprecated (autofallback to ztls enabled by default)

Config directory (v3, auto-migrated, no user action):
  - Linux:   $HOME/.config/nuclei
  - macOS:   $HOME/Library/Application Support/nuclei
  - Windows: %AppData%/nuclei
  (The `-config-directory` flag behavior changed in v3.)

Nuclei v3 headline features: Code protocol (bash/sh/python), template signing &
verification (ECDSA), JavaScript protocol (goja), multi-protocol engine, flow engine, SDK-4-ALL.


======================================================================
## VERBATIM DOC: templates_introduction.md
======================================================================
> ## Documentation Index
> Fetch the complete documentation index at: https://docs.projectdiscovery.io/llms.txt
> Use this file to discover all available pages before exploring further.

# Introduction to Nuclei Templates

> YAML based universal language for describing exploitable vulnerabilities

<Info>
  Write and test Nuclei templates directly in your browser using our [template editor](https://cloud.projectdiscovery.io/templates/editor). The editor supports AI-assisted template generation, real-time validation, and immediate scanning against your targets. Need automation? Check out our [template generation API](/api-reference/templates/generate-ai-template).
</Info>

## What are Nuclei Templates?

Nuclei templates are the cornerstone of the Nuclei scanning engine. Nuclei templates enable precise and rapid scanning across various protocols like TCP, DNS, HTTP, and more. They are designed to send targeted requests based on specific vulnerability checks, ensuring low-to-zero false positives and efficient scanning over large networks.

## YAML

Nuclei templates are based on the concepts of `YAML` based template files that define how the requests will be sent and processed. This allows easy extensibility capabilities to nuclei. The templates are written in `YAML` which specifies a simple human-readable format to quickly define the execution process.

## Universal Language for Vulnerabilities

Nuclei Templates offer a streamlined way to identify and communicate vulnerabilities, combining essential details like severity ratings and detection methods. This open-source, community-developed tool accelerates threat response and is widely recognized in the cybersecurity world.

<Tip>
  Learn more about nuclei templates as a universal language for exploitable vulnerabilities [on our blog](https://projectdiscovery.io/blog/the-power-of-nuclei-templates-a-universal-language-of-vulnerabilities/).
</Tip>

## Learn more

Let's dive into the world of Nuclei templates! Use the links on the left or those below to learn more.

<CardGroup cols={2}>
  <Card title="Structure" icon="table-tree" iconType="regular" href="/templates/structure">
    Learn what makes up the structure of a nuclei template
  </Card>

  <Card title="Basic HTTP" icon="globe" iconType="solid" href="/templates/protocols/http/basic-http">
    Get started making simple HTTP requests with Nuclei
  </Card>

  <Card title="Writing your first template" icon="video" iconType="solid" href="https://www.youtube.com/watch?v=nFXygQdtjyw">
    Watch a video on writing your first nuclei template!
  </Card>

  <Card title="Contributing" icon="github" iconType="solid" href="https://github.com/projectdiscovery">
    Nuclei thrives on community contributions. Submit your templates to be used by security experts everywhere!
  </Card>
</CardGroup>

======================================================================
## VERBATIM DOC: templates_protocols_http_basic-http.md
======================================================================
> ## Documentation Index
> Fetch the complete documentation index at: https://docs.projectdiscovery.io/llms.txt
> Use this file to discover all available pages before exploring further.

# Basic HTTP Protocol

> Learn about using Basic HTTP with Nuclei

Nuclei offers extensive support for various features related to HTTP protocol. Raw and Model based HTTP requests are supported, along with options Non-RFC client requests support too. Payloads can also be specified and raw requests can be transformed based on payload values along with many more capabilities that are shown later on this Page.

HTTP Requests start with a `request` block which specifies the start of the requests for the template.

```yaml theme={null}
# Start the requests for the template right here
http:
```

## Method

Request method can be **GET**, **POST**, **PUT**, **DELETE**, etc. depending on the needs.

```yaml theme={null}
# Method is the method for the request
method: GET
```

<Note>
  **Redirects**

  Redirection conditions can be specified per each template. By default, redirects are not followed. However, if desired, they can be enabled with `redirects: true` in request details. 10 redirects are followed at maximum by default which should be good enough for most use cases. More fine grained control can be exercised over number of redirects followed by using `max-redirects` field.
</Note>

An example of the usage:

```yaml theme={null}
http:
  - method: GET
    path:
      - "{{BaseURL}}/login.php"
    redirects: true
    max-redirects: 3
```

<Warning>Currently redirects are defined per template, not per request.</Warning>

## Path

The next part of the requests is the **path** of the request path. Dynamic variables can be placed in the path to modify its behavior on runtime.

Variables start with `{{` and end with `}}` and are case-sensitive.

`{{BaseURL}}` - This will replace on runtime in the request by the input URL as specified in the target file.

`{{RootURL}}` - This will replace on runtime in the request by the root URL as specified in the target file.

`{{Hostname}}` - Hostname variable is replaced by the hostname including port of the target on runtime.

`{{Host}}` - This will replace on runtime in the request by the input host as specified in the target file.

`{{Port}}` - This will replace on runtime in the request by the input port as specified in the target file.

`{{Path}}` - This will replace on runtime in the request by the input path as specified in the target file.

`{{File}}` - This will replace on runtime in the request by the input filename as specified in the target file.

`{{Scheme}}` - This will replace on runtime in the request by protocol scheme as specified in the target file.

An example is provided below - [https://example.com:443/foo/bar.php](https://example.com:443/foo/bar.php)

| Variable       | Value                                                                      |
| -------------- | -------------------------------------------------------------------------- |
| `{{BaseURL}}`  | [https://example.com:443/foo/bar.php](https://example.com:443/foo/bar.php) |
| `{{RootURL}}`  | [https://example.com:443](https://example.com:443)                         |
| `{{Hostname}}` | example.com:443                                                            |
| `{{Host}}`     | example.com                                                                |
| `{{Port}}`     | 443                                                                        |
| `{{Path}}`     | /foo                                                                       |
| `{{File}}`     | bar.php                                                                    |
| `{{Scheme}}`   | https                                                                      |

Some sample dynamic variable replacement examples:

```yaml theme={null}
path: "{{BaseURL}}/.git/config"
# This path will be replaced on execution with BaseURL
# If BaseURL is set to  https://abc.com then the
# path will get replaced to the following: https://abc.com/.git/config
```

Multiple paths can also be specified in one request which will be requested for the target.

## Headers

Headers can also be specified to be sent along with the requests. Headers are placed in form of key/value pairs. An example header configuration looks like this:

```yaml theme={null}
# headers contain the headers for the request
headers:
  # Custom user-agent header
  User-Agent: Some-Random-User-Agent
  # Custom request origin
  Origin: https://google.com
```

## Body

Body specifies a body to be sent along with the request. For instance:

```yaml theme={null}
# Body is a string sent along with the request
body: "{\"some random JSON\"}"

# Body is a string sent along with the request
body: "admin=test"
```

## Session

To maintain a cookie-based browser-like session between multiple requests, cookies are reused by default. This is beneficial when you want to maintain a session between a series of requests to complete the exploit chain or to perform authenticated scans. If you need to disable this behavior, you can use the disable-cookie field.

```yaml theme={null}
# disable-cookie accepts boolean input and false as default
disable-cookie: true
```

## Request Condition

Request condition allows checking for the condition between multiple requests for writing complex checks and exploits involving various HTTP requests to complete the exploit chain.

The functionality will be automatically enabled if DSL matchers/extractors contain numbers as a suffix with respective attributes.

For example, the attribute `status_code` will point to the effective status code of the current request/response pair in elaboration. Previous responses status codes are accessible by suffixing the attribute name with `_n`, where n is the n-th ordered request 1-based. So if the template has four requests and we are currently at number 3:

* `status_code`: will refer to the response code of request number 3
* `status_code_1` and `status_code_2` will refer to the response codes of the sequential responses number one and two

For example with `status_code_1`, `status_code_3`, and`body_2`:

```yaml theme={null}
    matchers:
      - type: dsl
        dsl:
          - "status_code_1 == 404 && status_code_2 == 200 && contains((body_2), 'secret_string')"
```

<Note>Request conditions might require more memory as all attributes of previous responses are kept in memory</Note>

## Example HTTP Template

The final template file for the `.git/config` file mentioned above is as follows:

```yaml theme={null}
id: git-config

info:
  name: Git Config File
  author: Ice3man
  severity: medium
  description: Searches for the pattern /.git/config on passed URLs.

http:
  - method: GET
    path:
      - "{{BaseURL}}/.git/config"
    matchers:
      - type: word
        words:
          - "[core]"
```

<Tip>
  More complete examples are provided [here](/templates/protocols/http/basic-http-examples)
</Tip>

======================================================================
## VERBATIM DOC: templates_protocols_network.md
======================================================================
> ## Documentation Index
> Fetch the complete documentation index at: https://docs.projectdiscovery.io/llms.txt
> Use this file to discover all available pages before exploring further.

# Network Protocol

> Learn about network requests with Nuclei

Nuclei can act as an automatable **Netcat**, allowing users to send bytes across the wire and receive them, while providing matching and extracting capabilities on the response.

Network Requests start with a **network** block which specifies the start of the requests for the template.

```yaml theme={null}
# Start the requests for the template right here
tcp:
```

### Inputs

First thing in the request is **inputs**. Inputs are the data that will be sent to the server, and optionally any data to read from the server.

At its most simple, just specify a string, and it will be sent across the network socket.

```yaml theme={null}
# inputs is the list of inputs to send to the server
inputs: 
  - data: "TEST\r\n"
```

You can also send hex encoded text that will be first decoded and the raw bytes will be sent to the server.

```yaml theme={null}
inputs:
  - data: "50494e47"
    type: hex
  - data: "\r\n"
```

Helper function expressions can also be defined in input and will be first evaluated and then sent to the server. The last Hex Encoded example can be sent with helper functions this way -

```yaml theme={null}
inputs:
  - data: 'hex_decode("50494e47")\r\n'
```

One last thing that can be done with inputs is reading data from the socket. Specifying `read-size` with a non-zero value will do the trick. You can also assign the read data some name, so matching can be done on that part.

```yaml theme={null}
inputs:
  - read-size: 8
```

Example with reading a number of bytes, and only matching on them.

```yaml theme={null}
inputs:
  - read-size: 8
    name: prefix
...
matchers:
  - type: word
    part: prefix
    words: 
      - "CAFEBABE"
```

Multiple steps can be chained together in sequence to do network reading / writing.

### Host

The next part of the requests is the **host** to connect to. Dynamic variables can be placed in the path to modify its value on runtime. Variables start with `{{` and end with `}}` and are case-sensitive.

1. **Hostname** - variable is replaced by the hostname provided on command line.

An example name value:

```yaml theme={null}
host: 
  - "{{Hostname}}"
```

Nuclei can also do TLS connection to the target server. Just add `tls://` as prefix before the **Hostname** and you're good to go.

```yaml theme={null}
host:
  - "tls://{{Hostname}}"
```

If a port is specified in the host, the user supplied port is ignored and the template port takes precedence.

### Port

Starting from Nuclei v2.9.15, a new field called `port` has been introduced in network templates. This field allows users to specify the port separately instead of including it in the host field.

Previously, if you wanted to write a network template for an exploit targeting SSH, you would have to specify both the hostname and the port in the host field, like this:

```yaml theme={null}
host:
  - "{{Hostname}}"
  - "{{Host}}:22"
```

In the above example, two network requests are sent: one to the port specified in the input/target, and another to the default SSH port (22).

The reason behind introducing the port field is to provide users with more flexibility when running network templates on both default and non-default ports. For example, if a user knows that the SSH service is running on a non-default port of 2222 (after performing a port scan with service discovery), they can simply run:

```bash theme={null}
$ nuclei -u scanme.sh:2222 -id xyz-ssh-exploit
```

In this case, Nuclei will use port 2222 instead of the default port 22. If the user doesn't specify any port in the input, port 22 will be used by default. However, this approach may not be straightforward to understand and can generate warnings in logs since one request is expected to fail.

Another issue with the previous design of writing network templates is that requests can be sent to unexpected ports. For example, if a web service is running on port 8443 and the user runs:

```bash theme={null}
$ nuclei -u scanme.sh:8443
```

In this case, `xyz-ssh-exploit` template will send one request to `scanme.sh:22` and another request to `scanme.sh:8443`, which may return unexpected responses and eventually result in errors. This is particularly problematic in automation scenarios.

To address these issues while maintaining the existing functionality, network templates can now be written in the following way:

```yaml theme={null}
host:
  - "{{Hostname}}"
port: 22
```

In this new design, the functionality to run templates on non-standard ports will still exist, except for the default reserved ports (`80`, `443`, `8080`, `8443`, `8081`, `53`). Additionally, the list of default reserved ports can be customized by adding a new field called exclude-ports:

```yaml theme={null}
exclude-ports: 80,443
```

When `exclude-ports` is used, the default reserved ports list will be overwritten. This means that if you want to run a network template on port `80`, you will have to explicitly specify it in the port field.

Starting from Nuclei v3.1.0 `port` field supports comma seperated values and multi ports can be specified in the port field. For example, if you want to run a network template on port `5432` and `5433`, you can specify it in the port field like this:

```yaml theme={null}
port: 5432,5433
```

In this case, Nuclei will first check if port is open from list and run template only on open ports

#### Matchers / Extractor Parts

Valid `part` values supported by **Network** protocol for Matchers / Extractor are -

| Value            | Description                         |
| ---------------- | ----------------------------------- |
| request          | Network Request                     |
| data             | Final Data Read From Network Socket |
| raw / body / all | All Data received from Socket       |

### **Example Network Template**

The final example template file for a `hex` encoded input to detect MongoDB running on servers with working matchers is provided below.

```yaml theme={null}
id: input-expressions-mongodb-detect

info:
  name: Input Expression MongoDB Detection
  author: pdteam
  severity: info
  reference: https://github.com/orleven/Tentacle

tcp:
  - inputs:
      - data: "{{hex_decode('3a000000a741000000000000d40700000000000061646d696e2e24636d640000000000ffffffff130000001069736d6173746572000100000000')}}"
    host:
      - "{{Hostname}}"
    port: 27017
    read-size: 2048
    matchers:
      - type: word
        words:
          - "logicalSessionTimeout"
          - "localTime"
```

<Tip>
  More complete examples are provided [here](/templates/protocols/network-examples).
</Tip>

======================================================================
## VERBATIM DOC: templates_protocols_flow.md
======================================================================
> ## Documentation Index
> Fetch the complete documentation index at: https://docs.projectdiscovery.io/llms.txt
> Use this file to discover all available pages before exploring further.

# Flow Protocol

> Learn about the template flow engine in Nuclei v3

## Overview

The template flow engine was introduced in nuclei v3, and brings two significant enhancements to Nuclei:

* The ability to [conditionally execute requests](#conditional-execution)
* The [orchestration of request execution](#request-execution-orchestration)

These features are implemented using JavaScript (ECMAScript 5.1) via the [goja](https://github.com/dop251/goja) backend.

## Conditional Execution

Many times when writing complex templates we might need to add some extra checks (or conditional statements) before executing certain part of request.

An ideal example of this would be when [bruteforcing wordpress login](https://cloud.projectdiscovery.io/public/wordpress-weak-credentials) with default usernames and passwords, but if we carefully re-evaluate this template, we can see that template is sending 276 requests without even checking, if the url actually exists or the target site is actually a wordpress site.

With addition of flow in Nuclei v3 we can re-write this template to first check if the target is a wordpress site, if yes then bruteforce login with default credentials and this can be achieved by simply adding one line of content  i.e `flow: http(1) && http(2)` and nuclei will take care of everything else.

```yaml theme={null}
id: wordpress-bruteforce

info:
  name: WordPress Login Bruteforce
  author: pdteam
  severity: high

flow: http(1) && http(2)

http:
  - method: GET
    path:
      - "{{BaseURL}}/wp-login.php"

    matchers:
      - type: word
        words:
          - "WordPress"

  - method: POST
    path:
      - "{{BaseURL}}/wp-login.php"

    body: |
        log={{username}}&pwd={{password}}&wp-submit=Log+In

    attack: clusterbomb 
    payloads:
      users: helpers/wordlists/wp-users.txt
      passwords: helpers/wordlists/wp-passwords.txt

    matchers:
      - type: dsl
        dsl:
          - status_code == 302
          - contains_all(header, "/wp-admin","wordpress_logged_in")
        condition: and
```

The update template now seems straight forward and easy to understand. we are first checking if the target is a wordpress site and then executing bruteforce requests. This is just a simple example of conditional execution and flow accepts any Javascript (ECMAScript 5.1) expression/code so you are free to craft any conditional execution logic you want.

## Request Execution Orchestration

Flow is a powerful Nuclei feature that provides enhanced orchestration capabilities for executing requests. The simplicity of conditional execution is just the beginning. With ﻿flow, you can:

* Iterate over a list of values and execute a request for each one
* Extract values from a request, iterate over them, and perform another request for each
* Get and set values within the template context (global variables)
* Write output to stdout for debugging purposes or based on specific conditions
* Introduce custom logic during template execution
* Use ECMAScript 5.1 JavaScript features to build and modify variables at runtime
* Update variables at runtime and use them in subsequent requests.

Think of request execution orchestration as a bridge between JavaScript and Nuclei, offering two-way interaction within a specific template.

**Practical Example: Vhost Enumeration**

To better illustrate the power of ﻿flow, let's consider developing a template for vhost (virtual host) enumeration. This set of tasks typically requires writing a new tool from scratch. Here are the steps we need to follow:

1. Retrieve the SSL certificate for the provided IP (using tlsx)
   * Extract `subject_cn` (CN) from the certificate
   * Extract `subject_an` (SAN) from the certificate
   * Remove wildcard prefixes from the values obtained in the steps above
2. Bruteforce the request using all the domains found from the SSL request

You can utilize flow to simplify this task. The JavaScript code below orchestrates the vhost enumeration:

```javascript theme={null}
ssl();
for (let vhost of iterate(template["ssl_domains"])) {
    set("vhost", vhost);
    http();
}
```

In this code, we've introduced 5 extra lines of JavaScript. This allows the template to perform vhost enumeration. The best part? You can run this at scale with all features of Nuclei, using supported inputs like ﻿ASN, ﻿CIDR, ﻿URL.

Let's break down the JavaScript code:

1. `ssl()`: This function executes the SSL request.
2. `template["ssl_domains"]`: Retrieves the value of `ssl_domains` from the template context.
3. `iterate()`: Helper function that iterates over any value type while handling empty or null values.
4. `set("vhost", vhost)`: Creates a new variable `vhost` in the template and assigns the `vhost` variable's value to it.
5. `http()`: This function conducts the HTTP request.

By understanding and taking advantage of Nuclei's `flow`, you can redefine the way you orchestrate request executions, making your templates much more powerful and efficient.

Here is working template for vhost enumeration using flow:

```yaml theme={null}
id: vhost-enum-flow

info:
  name: vhost enum flow
  author: tarunKoyalwar
  severity: info
  description: |
    vhost enumeration by extracting potential vhost names from ssl certificate.

flow: |
  ssl();
  for (let vhost of iterate(template["ssl_domains"])) {
    set("vhost", vhost);
    http();
  }

ssl:
  - address: "{{Host}}:{{Port}}"

http:
  - raw:
      - |
        GET / HTTP/1.1
        Host: {{vhost}}

    matchers:
      - type: dsl
        dsl:
          - status_code != 400
          - status_code != 502

    extractors:
      - type: dsl
        dsl:
          - '"VHOST: " + vhost + ", SC: " + status_code + ", CL: " + content_length'
```

## JS Bindings

This section contains a brief description of all nuclei JS bindings and their usage.

### Protocol Execution Function

In nuclei, any listed protocol can be invoked or executed in JavaScript using the `protocol_name()` format. For example, you can use `http()`, `dns()`, `ssl()`, etc.

If you want to execute a specific request of a protocol (refer to nuclei-flow-dns for an example), it can be achieved by passing either:

* The index of that request in the protocol (e.g.,`dns(1)`, `dns(2)`)
* The ID of that request in the protocol (e.g., `dns("extract-vps")`, `http("probe-http")`)

For more advanced scenarios where multiple requests of a single protocol need to be executed, you can specify their index or ID one after the other (e.g., ﻿dns("extract-vps","1")).

This flexibility in using either index numbers or ID strings to call specific protocol requests provides controls for tailored execution, allowing you to build more complex and efficient workflows. more complex use cases multiple requests of a single protocol can be executed by just specifying their index or id one after another (ex: `dns("extract-vps","1")`)

### Iterate Helper Function

Iterate is a nuclei js helper function which can be used to iterate over any type of value like **array**, **map**, **string**, **number** while handling empty/nil values.

This is addon helper function from nuclei to omit boilerplate code of checking if value is empty or not and then iterating over it

```javascript theme={null}
iterate(123,{"a":1,"b":2,"c":3})

// iterate over array with custom separator
iterate([1,2,3,4,5], " ")
```

### Set Helper Function

When iterating over a values/array or some other use case we might want to invoke a request with custom/given value and this can be achieved by using `set()` helper function. When invoked/called it adds given variable to template context (global variables) and that value is used during execution of request/protocol. the format of `set()` is `set("variable_name",value)` ex: `set("username","admin")`.

```javascript theme={null}
for (let vhost of myArray) {
  set("vhost", vhost);
  http(1)
}
```

**Note:** In above example we used `set("vhost", vhost)` which added `vhost` to template context (global variables) and then called `http(1)` which used this value in request.

### Template Context

A template context is nothing but a map/jsonl containing all this data along with internal/unexported data that is only available at runtime (ex: extracted values from previous requests, variables added using `set()` etc). This template context is available in javascript as `template` variable and can be used to access any data from it. ex: `template["dns_cname"]`, `template["ssl_subject_cn"]` etc.

```javascript theme={null}
template["ssl_domains"] // returns value of ssl_domains from template context which is available after executing ssl request 
template["ptrValue"]  // returns value of ptrValue which was extracted using regex with internal: true
```

Lot of times we don't known what all data is available in template context and this can be easily found by printing it to stdout using `log()` function

```javascript theme={null}
log(template)
```

### Log Helper Function

It is a nuclei js alternative to `console.log` and this pretty prints map data in readable format

**Note:** This should be used for debugging purposed only as this prints data to stdout

### Dedupe

Lot of times just having arrays/slices is not enough and we might need to remove duplicate variables . for example in earlier vhost enumeration we did not remove any duplicates as there is always a chance of duplicate values in `ssl_subject_cn` and `ssl_subject_an` and this can be achieved by using `dedupe()` object. This is nuclei js helper function to abstract away boilerplate code of removing duplicates from array/slice

```javascript theme={null}
let uniq = new Dedupe(); // create new dedupe object
uniq.Add(template["ptrValue"]) 
uniq.Add(template["ssl_subject_cn"]);
uniq.Add(template["ssl_subject_an"]); 
log(uniq.Values())
```

And that's it, this automatically converts any slice/array to map and removes duplicates from it and returns a slice/array of unique values

> Similar to DSL helper functions . we can either use built in functions available with `Javscript (ECMAScript 5.1)` or use DSL helper functions and its upto user to decide which one to uses.

### Skip Internal Matchers in MultiProtocol / Flow Templates

Before nuclei v3.1.4 , A template like [`CVE-2023-43177`](https://github.com/projectdiscovery/nuclei-templates/blob/c5be73e328ebd9a0c122ea0324f60bbdd7eb940d/http/cves/2023/CVE-2023-43177.yaml#L28) which has multiple requests/protocols and uses `flow` for logic, used to only return one result but it conflicted with logic when `for` loop was used in `flow` to fix this nuclei engine from v3.1.4 will print all events/results in a template and template writers can use `internal: true` in matchers to skip printing of events/results just like dynamic extractors.

Note: this is only relevant if matchers/extractors are used in previous requests/protocols

Example of [`CVE-2023-6553`](https://github.com/projectdiscovery/nuclei-templates/blob/c5be73e328ebd9a0c122ea0324f60bbdd7eb940d/http/cves/2023/CVE-2023-6553.yaml#L21) with new `internal: true` logic would be

```yaml theme={null}
id: CVE-2023-6553

info:
  name: Worpress Backup Migration <= 1.3.7 - Unauthenticated Remote Code Execution
  author: FLX
  severity: critical

flow: http(1) && http(2)

http:
  - method: GET
    path:
      - "{{BaseURL}}/wp-content/plugins/backup-backup/readme.txt"

    matchers:
      - type: dsl
        dsl:
          - 'status_code == 200'
          - 'contains(body, "Backup Migration")'
        condition: and
        internal: true  # <- updated logic (this will skip printing this event/result)

  - method: POST
    path:
      - "{{BaseURL}}/wp-content/plugins/backup-backup/includes/backup-heart.php"
    headers:
      Content-Dir: "{{rand_text_alpha(10)}}"

    matchers:
      - type: dsl
        dsl:
          - 'len(body) == 0'
          - 'status_code == 200'
          - '!contains(body, "Incorrect parameters")'
        condition: and
```

======================================================================
## VERBATIM DOC: opensource_nuclei_running.md
======================================================================
> ## Documentation Index
> Fetch the complete documentation index at: https://docs.projectdiscovery.io/llms.txt
> Use this file to discover all available pages before exploring further.

# Running Nuclei

> Learn about how to run Nuclei and produce results

<iframe src="https://www.youtube.com/embed/b5qMyQvL1ZA" width="640" height="360" />

## How to Run Nuclei

Nuclei templates offer two primary execution methods:

### Supported Input Formats

For automation in pipelines, see [Running Nuclei in CI/CD](/opensource/nuclei/ci-cd).

Nuclei supports various input formats to run template against, including urls, hosts, ips, cidrs, asn, openapi, swagger, proxify, burpsuite exported data and more. To learn more on using input specify options, you can refer [nuclei input formats](/opensource/nuclei/input-formats).

These inputs can be given to nuclei using `-l` and `-input-mode` flags.

```console theme={null}
  -l, -list string              path to file containing a list of target URLs/hosts to scan (one per line)
  -im, -input-mode string       mode of input file (list, burp, jsonl, yaml, openapi, swagger) (default "list")
```

Executing nuclei against a list of inputs (urls, hosts, ips, cidrs, asn) is as simple as running the following command:

```bash theme={null}
  nuclei -l targets.txt
```

For running other input formats (burp, jsonl, yaml, openapi, swagger), you can use the `-im` flag to specify the input mode.

```bash theme={null}
  nuclei -l targets.burp -im burp
```

```bash theme={null}
  nuclei -l openapi.yaml -im openapi
```

and so on.

### Executing Nuclei Templates

`-t/templates`

**Default Templates**

Most community templates from our [nuclei-template repository](https://github.com/projectdiscovery/nuclei-templates) are executed by default, directly from the standard installation path. The typical command is as follows:

```sh theme={null}
nuclei -u https://example.com
```

However, there are some exceptions regarding the templates that run by default:

* Certain tags and templates listed in the [default `.nuclei-ignore` file](https://github.com/projectdiscovery/nuclei-templates/blob/main/.nuclei-ignore) are not included.
* [Code Templates](/templates/protocols/code) require the `-code` flag to execute.
* [Headless Templates](/templates/protocols/headless) will not run unless you pass the `-headless` flag.
* [Fuzzing Templates](/template/protocols/http/fuzzing-overview) will not run unless you pass the `-fuzz` flag.

You can also run templates against a list of URLs:

```sh theme={null}
nuclei -list http_urls.txt
```

**Custom Templates**

To run a custom template directory or multiple directories, use the following command structure:

```sh theme={null}
nuclei -u https://example.com -t cves/ -t exposures/
```

Templates from custom GitHub repositories, stored under the github directory, can be executed with this command:

```sh theme={null}
nuclei -u https://example.com -t github/private-repo
```

You can also directly run a template from any ProjectDiscovery Cloud Platform URL like this:

```sh theme={null}
nuclei -u https://example.com -t https://cloud.projectdiscovery.io/public/tech-detect
```

### Executing Template Workflows

`-w/workflows`

[Workflows](/templates/workflows/overview) can be executed using the following command:

```sh theme={null}
nuclei -u https://example.com -w workflows/
```

Similarly, Workflows can be executed against a list of URLs.

```sh theme={null}
nuclei -list http_urls.txt -w workflows/wordpress-workflow.yaml
```

## Types of Templates

### Template **Filters**

Nuclei engine supports three basic filters to customize template execution.

1. Tags (`-tags`)

   Filter based on tags field available in the template.

2. Severity (`-severity`)

   Filter based on severity field available in the template.

3. Author (`-author`)

   Filter based on author field available in the template.

As default, Filters are applied on installed path of templates and can be customized with manual template path input.

For example, below command will run all the templates installed at `~/nuclei-templates/` directory and has `cve` tags in it.

```sh theme={null}
nuclei -u https://example.com -tags cve
```

And this example will run all the templates available under `~/nuclei-templates/exposures/` directory and has `config` tag in it.

```sh theme={null}
nuclei -u https://example.com -tags config -t exposures/
```

Multiple filters works together with AND condition,
below example runs all templates with `cve` tags
AND has `critical` OR `high` severity AND `geeknik` as author of template.

```sh theme={null}
nuclei -u https://example.com -tags cve -severity critical,high -author geeknik
```

### Advanced Filters

Multiple filters can also be combined using the template condition flag (`-tc`) that allows complex expressions like the following ones:

```sh theme={null}
nuclei -tc "contains(id,'xss') || contains(tags,'xss')"
nuclei -tc "contains(tags,'cve') && contains(tags,'ssrf')"
nuclei -tc "contains(name, 'Local File Inclusion')"
```

The supported fields are:

* `id` string
* `name` string
* `description` string
* `tags` slice of strings
* `authors` slice of strings
* `severity` string
* `protocol` string
* `http_method` slice of strings
* `body` string (containing all request bodies if any)
* `matcher_type` slice of string
* `extractor_type` slice of string
* `description` string

Also, every key-value pair from the template metadata section is accessible. All fields can be combined with logical operators (`||` and `&&`) and used with DSL helper functions.

Similarly, all filters are supported in workflows as well.

```sh theme={null}
nuclei -w workflows/wordpress-workflow.yaml -severity critical,high -list http_urls.txt
```

<Note>
  **Workflows**

  In Workflows, Nuclei filters are applied on templates or sub-templates running via workflows, not on the workflows itself.
</Note>

### Public Templates

Nuclei has built-in support for automatic template download/update from [**nuclei templates**](https://github.com/projectdiscovery/nuclei-templates) project which provides [community-contributed](https://github.com/projectdiscovery/nuclei-templates#-community) list of ready-to-use templates that is constantly updated.

Nuclei checks for new community template releases upon each execution and automatically downloads the latest version when available. optionally, this feature can be disabled using the `-duc` cli flag or the configuration file.

### Custom Templates

Users can create custom templates on a personal public / private GitHub / AWS Bucket that they wish to run / update while using nuclei from any environment without manually downloading the GitHub repository everywhere.

To use this feature, users need to set the following environment variables:

<AccordionGroup>
  <Accordion title="For GitHub Project" icon="pencil">
    ```bash theme={null}
    export GITHUB_TOKEN=gh_XXX
    export GITHUB_TEMPLATE_REPO=my_nuclei_template
    ```
  </Accordion>

  <Accordion title="For GitLab Project" icon="pencil">
    ```bash theme={null}
    export GITLAB_SERVER_URL=https://gitlab.com
    # The GitLab token must have the read_api and read_repository scope
    export GITLAB_TOKEN=XXXXXXXXXX
    # Comma separated list of repository IDs (not names)
    export GITLAB_REPOSITORY_IDS=12345,67890
    ```
  </Accordion>

  <Accordion title="For AWS Bucket" icon="pencil">
    ```bash theme={null}
    export AWS_ACCESS_KEY=AKIAXXXXXXXX
    export AWS_SECRET_KEY=XXXXXX
    export AWS_REGION=us-xxx-1
    export AWS_TEMPLATE_BUCKET=aws_bucket_name
    ```
  </Accordion>

  <Accordion title="For Azure Blob Storage" icon="pencil">
    ```bash theme={null}
    export AZURE_TENANT_ID=00000000-0000-0000-0000-000000000000
    export AZURE_CLIENT_ID=00000000-0000-0000-0000-000000000000
    export AZURE_CLIENT_SECRET=00000000-0000-0000-0000-000000000000
    export AZURE_SERVICE_URL=https://XXXXXXXXXX.blob.core.windows.net/
    export AZURE_CONTAINER_NAME=templates
    ```
  </Accordion>
</AccordionGroup>

Environment variables can also be provided to disable download from default and custom template locations:

```bash theme={null}
# Disable download from the default nuclei-templates project
export DISABLE_NUCLEI_TEMPLATES_PUBLIC_DOWNLOAD=true

# Disable download from public / private GitHub project(s)
export DISABLE_NUCLEI_TEMPLATES_GITHUB_DOWNLOAD=true

# Disable download from public / private GitLab project(s)
export DISABLE_NUCLEI_TEMPLATES_GITLAB_DOWNLOAD=true

# Disable download from public / private AWS Bucket(s)
export DISABLE_NUCLEI_TEMPLATES_AWS_DOWNLOAD=true

# Disable download from public / private Azure Blob Storage
export DISABLE_NUCLEI_TEMPLATES_AZURE_DOWNLOAD=true
```

Once the environment variables are set, following command to download the custom templates:

```bash theme={null}
nuclei -update-templates
```

This command will clone the repository containing the custom templates to the default nuclei templates directory (`$HOME/nuclei-templates/github/`).

The directory structure of the custom templates looks as follows:

```bash theme={null}
tree $HOME/nuclei-templates/

nuclei-templates/
└── github/$GH_REPO_NAME # Custom templates downloaded from public / private GitHub project
└── gitlab/$GL_REPO_NAME # Custom templates downloaded from public / private GitLab project
└── s3/$BUCKET_NAME # Custom templates downloaded from public / private AWS Bucket
└── azure/$CONTAINER_NAME # Custom templates downloaded from public / private Azure Blob Storage
```

Users can then use the custom templates with the `-t` flag as follows:

```
nuclei -t github/my_custom_template -u https://example.com
```

The nuclei engine can be updated to latest version by using the `-update` flag.

<Tip>
  Writing your own unique templates will always keep you one step ahead of
  others.
</Tip>

### AI-Powered Template Generation

`-ai`

Nuclei supports generating and running templates on-the-fly using AI capabilities powered by the ProjectDiscovery API. This feature allows you to perform quick, targeted scans without needing pre-written templates by describing what you want to detect in natural language.

**Prerequisites:**

1. A ProjectDiscovery API key (Get one at [cloud.projectdiscovery.io](https://cloud.projectdiscovery.io))
2. Configure your API key using one of these methods:

   **Method 1: Using CLI (Recommended)**

   ```bash theme={null}
   nuclei -auth
   # Enter your API key when prompted
   ```

   **Method 2: Environment Variable**

   ```bash theme={null}
   export PDCP_API_KEY=your_api_key_here
   ```

**Basic Usage:**

1. **Finding Sensitive Information Leaks:**

```bash theme={null}
nuclei -list targets.txt -ai "Find admin_api_key in response"
```

2. **Detecting Debug Information:**

```bash theme={null}
nuclei -list targets.txt -ai "Detect exposed stack traces in error messages"
```

3. **Discovering Admin Interfaces:**

```bash theme={null}
nuclei -list targets.txt -ai "Find admin login endpoints"
```

4. **Identifying Exposed Secrets:**

```bash theme={null}
nuclei -list urls.txt -ai "Detect secrets in response"
```

5. **Extract Page Titles**

```bash theme={null}
nuclei -list targets.txt -ai "Extract page titles"
```

<Note>
  The `-ai` flag requires an active internet connection to communicate with the ProjectDiscovery API. Generated templates are stored both locally on your computer and in your ProjectDiscovery cloud account for future reference. For privacy, your prompts and generated templates are not used for AI training.

  Currently, each user is limited to 100 AI template generation queries per day. This limit is subject to change based on usage patterns and to prevent abuse.
</Note>

### Nuclei Flags

```
nuclei -h
```

This will display help for the tool. Here are all the switches it supports.

```console theme={null}
Nuclei is a fast, template based vulnerability scanner focusing
on extensive configurability, massive extensibility and ease of use.

Usage:
  nuclei [flags]

Flags:
TARGET:
   -u, -target string[]          target URLs/hosts to scan
   -l, -list string              path to file containing a list of target URLs/hosts to scan (one per line)
   -eh, -exclude-hosts string[]  hosts to exclude to scan from the input list (ip, cidr, hostname)
   -resume string                resume scan using resume.cfg (clustering will be disabled)
   -sa, -scan-all-ips            scan all the IP's associated with dns record
   -iv, -ip-version string[]     IP version to scan of hostname (4,6) - (default 4)

TARGET-FORMAT:
   -im, -input-mode string        mode of input file (list, burp, jsonl, yaml, openapi, swagger) (default "list")
   -ro, -required-only            use only required fields in input format when generating requests
   -sfv, -skip-format-validation  skip format validation (like missing vars) when parsing input file

TEMPLATES:
   -nt, -new-templates                    run only new templates added in latest nuclei-templates release
   -ntv, -new-templates-version string[]  run new templates added in specific version
   -as, -automatic-scan                   automatic web scan using wappalyzer technology detection to tags mapping
   -t, -templates string[]                list of template or template directory to run (comma-separated, file)
   -turl, -template-url string[]          template url or list containing template urls to run (comma-separated, file)
   -ai, -prompt string                    generate and run template using ai prompt
   -w, -workflows string[]                list of workflow or workflow directory to run (comma-separated, file)
   -wurl, -workflow-url string[]          workflow url or list containing workflow urls to run (comma-separated, file)
   -validate                              validate the passed templates to nuclei
   -nss, -no-strict-syntax                disable strict syntax check on templates
   -td, -template-display                 displays the templates content
   -tl                                    list all available templates
   -tgl                                   list all available tags
   -sign                                  signs the templates with the private key defined in NUCLEI_SIGNATURE_PRIVATE_KEY env variable
   -code                                  enable loading code protocol-based templates
   -dut, -disable-unsigned-templates      disable running unsigned templates or templates with mismatched signature
   -esc, -enable-self-contained           enable loading self-contained templates
   -egm, -enable-global-matchers          enable loading global matchers templates
   -file                                  enable loading file templates

FILTERING:
   -a, -author string[]               templates to run based on authors (comma-separated, file)
   -tags string[]                     templates to run based on tags (comma-separated, file)
   -etags, -exclude-tags string[]     templates to exclude based on tags (comma-separated, file)
   -itags, -include-tags string[]     tags to be executed even if they are excluded either by default or configuration
   -id, -template-id string[]         templates to run based on template ids (comma-separated, file, allow-wildcard)
   -eid, -exclude-id string[]         templates to exclude based on template ids (comma-separated, file)
   -it, -include-templates string[]   path to template file or directory to be executed even if they are excluded either by default or configuration
   -et, -exclude-templates string[]   path to template file or directory to exclude (comma-separated, file)
   -em, -exclude-matchers string[]    template matchers to exclude in result
   -s, -severity value[]              templates to run based on severity. Possible values: info, low, medium, high, critical, unknown
   -es, -exclude-severity value[]     templates to exclude based on severity. Possible values: info, low, medium, high, critical, unknown
   -pt, -type value[]                 templates to run based on protocol type. Possible values: dns, file, http, headless, tcp, workflow, ssl, websocket, whois, code, javascript
   -ept, -exclude-type value[]        templates to exclude based on protocol type. Possible values: dns, file, http, headless, tcp, workflow, ssl, websocket, whois, code, javascript
   -tc, -template-condition string[]  templates to run based on expression condition

OUTPUT:
   -o, -output string            output file to write found issues/vulnerabilities
   -sresp, -store-resp           store all request/response passed through nuclei to output directory
   -srd, -store-resp-dir string  store all request/response passed through nuclei to custom directory (default "output")
   -silent                       display findings only
   -nc, -no-color                disable output content coloring (ANSI escape codes)
   -j, -jsonl                    write output in JSONL(ines) format
   -irr, -include-rr -omit-raw   include request/response pairs in the JSON, JSONL, and Markdown outputs (for findings only) [DEPRECATED use -omit-raw] (default true)
   -or, -omit-raw                omit request/response pairs in the JSON, JSONL, and Markdown outputs (for findings only)
   -ot, -omit-template           omit encoded template in the JSON, JSONL output
   -nm, -no-meta                 disable printing result metadata in cli output
   -ts, -timestamp               enables printing timestamp in cli output
   -rdb, -report-db string       nuclei reporting database (always use this to persist report data)
   -ms, -matcher-status          display match failure status
   -me, -markdown-export string  directory to export results in markdown format
   -se, -sarif-export string     file to export results in SARIF format
   -je, -json-export string      file to export results in JSON format
   -jle, -jsonl-export string    file to export results in JSONL(ine) format
   -rd, -redact string[]         redact given list of keys from query parameter, request header and body

CONFIGURATIONS:
   -config string                        path to the nuclei configuration file
   -tp, -profile string                  template profile config file to run
   -tpl, -profile-list                   list community template profiles
   -fr, -follow-redirects                enable following redirects for http templates
   -fhr, -follow-host-redirects          follow redirects on the same host
   -mr, -max-redirects int               max number of redirects to follow for http templates (default 10)
   -dr, -disable-redirects               disable redirects for http templates
   -rc, -report-config string            nuclei reporting module configuration file
   -H, -header string[]                  custom header/cookie to include in all http request in header:value format (cli, file)
   -V, -var value                        custom vars in key=value format
   -r, -resolvers string                 file containing resolver list for nuclei
   -sr, -system-resolvers                use system DNS resolving as error fallback
   -dc, -disable-clustering              disable clustering of requests
   -passive                              enable passive HTTP response processing mode
   -fh2, -force-http2                    force http2 connection on requests
   -ev, -env-vars                        enable environment variables to be used in template
   -cc, -client-cert string              client certificate file (PEM-encoded) used for authenticating against scanned hosts
   -ck, -client-key string               client key file (PEM-encoded) used for authenticating against scanned hosts
   -ca, -client-ca string                client certificate authority file (PEM-encoded) used for authenticating against scanned hosts
   -sml, -show-match-line                show match lines for file templates, works with extractors only
   -ztls                                 use ztls library with autofallback to standard one for tls13 [Deprecated] autofallback to ztls is enabled by default
   -sni string                           tls sni hostname to use (default: input domain name)
   -dka, -dialer-keep-alive value        keep-alive duration for network requests.
   -lfa, -allow-local-file-access        allows file (payload) access anywhere on the system
   -lna, -restrict-local-network-access  blocks connections to the local / private network
   -i, -interface string                 network interface to use for network scan
   -at, -attack-type string              type of payload combinations to perform (batteringram,pitchfork,clusterbomb)
   -sip, -source-ip string               source ip address to use for network scan
   -rsr, -response-size-read int         max response size to read in bytes
   -rss, -response-size-save int         max response size to read in bytes (default 1048576)
   -reset                                reset removes all nuclei configuration and data files (including nuclei-templates)
   -tlsi, -tls-impersonate               enable experimental client hello (ja3) tls randomization
   -hae, -http-api-endpoint string       experimental http api endpoint

INTERACTSH:
   -iserver, -interactsh-server string  interactsh server url for self-hosted instance (default: oast.pro,oast.live,oast.site,oast.online,oast.fun,oast.me)
   -itoken, -interactsh-token string    authentication token for self-hosted interactsh server
   -interactions-cache-size int         number of requests to keep in the interactions cache (default 5000)
   -interactions-eviction int           number of seconds to wait before evicting requests from cache (default 60)
   -interactions-poll-duration int      number of seconds to wait before each interaction poll request (default 5)
   -interactions-cooldown-period int    extra time for interaction polling before exiting (default 5)
   -ni, -no-interactsh                  disable interactsh server for OAST testing, exclude OAST based templates

FUZZING:
   -ft, -fuzzing-type string           overrides fuzzing type set in template (replace, prefix, postfix, infix)
   -fm, -fuzzing-mode string           overrides fuzzing mode set in template (multiple, single)
   -fuzz                               enable loading fuzzing templates (Deprecated: use -dast instead)
   -dast                               enable / run dast (fuzz) nuclei templates
   -dts, -dast-server                  enable dast server mode (live fuzzing)
   -dtr, -dast-report                  write dast scan report to file
   -dtst, -dast-server-token string    dast server token (optional)
   -dtsa, -dast-server-address string  dast server address (default "localhost:9055")
   -dfp, -display-fuzz-points          display fuzz points in the output for debugging
   -fuzz-param-frequency int           frequency of uninteresting parameters for fuzzing before skipping (default 10)
   -fa, -fuzz-aggression string        fuzzing aggression level controls payload count for fuzz (low, medium, high) (default "low")
   -cs, -fuzz-scope string[]           in scope url regex to be followed by fuzzer
   -cos, -fuzz-out-scope string[]      out of scope url regex to be excluded by fuzzer

UNCOVER:
   -uc, -uncover                  enable uncover engine
   -uq, -uncover-query string[]   uncover search query
   -ue, -uncover-engine string[]  uncover search engine (shodan,censys,fofa,shodan-idb,quake,hunter,zoomeye,netlas,criminalip,publicwww,hunterhow,google,odin,binaryedge) (default shodan)
   -uf, -uncover-field string     uncover fields to return (ip,port,host) (default "ip:port")
   -ul, -uncover-limit int        uncover results to return (default 100)
   -ur, -uncover-ratelimit int    override ratelimit of engines with unknown ratelimit (default 60 req/min) (default 60)

RATE-LIMIT:
   -rl, -rate-limit int               maximum number of requests to send per second (default 150)
   -rld, -rate-limit-duration value   maximum number of requests to send per second (default 1s)
   -rlm, -rate-limit-minute int       maximum number of requests to send per minute (DEPRECATED)
   -bs, -bulk-size int                maximum number of hosts to be analyzed in parallel per template (default 25)
   -c, -concurrency int               maximum number of templates to be executed in parallel (default 25)
   -hbs, -headless-bulk-size int      maximum number of headless hosts to be analyzed in parallel per template (default 10)
   -headc, -headless-concurrency int  maximum number of headless templates to be executed in parallel (default 10)
   -jsc, -js-concurrency int          maximum number of javascript runtimes to be executed in parallel (default 120)
   -pc, -payload-concurrency int      max payload concurrency for each template (default 25)
   -prc, -probe-concurrency int       http probe concurrency with httpx (default 50)

OPTIMIZATIONS:
   -timeout int                     time to wait in seconds before timeout (default 10)
   -retries int                     number of times to retry a failed request (default 1)
   -ldp, -leave-default-ports       leave default HTTP/HTTPS ports (eg. host:80,host:443)
   -mhe, -max-host-error int        max errors for a host before skipping from scan (default 30)
   -te, -track-error string[]       adds given error to max-host-error watchlist (standard, file)
   -nmhe, -no-mhe                   disable skipping host from scan based on errors
   -project                         use a project folder to avoid sending same request multiple times
   -project-path string             set a specific project path (default "/var/folders/ny/g1md_dq528v3n6vlmp_77hpw0000gn/T/")
   -spm, -stop-at-first-match       stop processing HTTP requests after the first match (may break template/workflow logic)
   -stream                          stream mode - start elaborating without sorting the input
   -ss, -scan-strategy value        strategy to use while scanning(auto/host-spray/template-spray) (default auto)
   -irt, -input-read-timeout value  timeout on input read (default 3m0s)
   -nh, -no-httpx                   disable httpx probing for non-url input
   -no-stdin                        disable stdin processing

HEADLESS:
   -headless                        enable templates that require headless browser support (root user on Linux will disable sandbox)
   -page-timeout int                seconds to wait for each page in headless mode (default 20)
   -sb, -show-browser               show the browser on the screen when running templates with headless mode
   -ho, -headless-options string[]  start headless chrome with additional options
   -sc, -system-chrome              use local installed Chrome browser instead of nuclei installed
   -lha, -list-headless-action      list available headless actions

DEBUG:
   -debug                     show all requests and responses
   -dreq, -debug-req          show all sent requests
   -dresp, -debug-resp        show all received responses
   -p, -proxy string[]        list of http/socks5 proxy to use (comma separated or file input)
   -pi, -proxy-internal       proxy all internal requests
   -ldf, -list-dsl-function   list all supported DSL function signatures
   -tlog, -trace-log string   file to write sent requests trace log
   -elog, -error-log string   file to write sent requests error log
   -version                   show nuclei version
   -hm, -hang-monitor         enable nuclei hang monitoring
   -v, -verbose               show verbose output
   -profile-mem string        generate memory (heap) profile & trace files
   -vv                        display templates loaded for scan
   -svd, -show-var-dump       show variables dump for debugging
   -vdl, -var-dump-limit int  limit the number of characters displayed in var dump (default 255)
   -ep, -enable-pprof         enable pprof debugging server
   -tv, -templates-version    shows the version of the installed nuclei-templates
   -hc, -health-check         run diagnostic check up

UPDATE:
   -up, -update                      update nuclei engine to the latest released version
   -ut, -update-templates            update nuclei-templates to latest released version
   -ud, -update-template-dir string  custom directory to install / update nuclei-templates
   -duc, -disable-update-check       disable automatic nuclei/templates update check

STATISTICS:
   -stats                    display statistics about the running scan
   -sj, -stats-json          display statistics in JSONL(ines) format
   -si, -stats-interval int  number of seconds to wait between showing a statistics update (default 5)
   -mp, -metrics-port int    port to expose nuclei metrics on (default 9092)
   -hps, -http-stats         enable http status capturing (experimental)

CLOUD:
   -auth                           configure projectdiscovery cloud (pdcp) api key (default true)
   -tid, -team-id string           upload scan results to given team id (optional) (default "none")
   -cup, -cloud-upload             upload scan results to pdcp dashboard [DEPRECATED use -dashboard]
   -sid, -scan-id string           upload scan results to existing scan id (optional)
   -sname, -scan-name string       scan name to set (optional)
   -pd, -dashboard                 upload / view nuclei results in projectdiscovery cloud (pdcp) UI dashboard
   -pdu, -dashboard-upload string  upload / view nuclei results file (jsonl) in projectdiscovery cloud (pdcp) UI dashboard

AUTHENTICATION:
   -sf, -secret-file string[]  path to config file containing secrets for nuclei authenticated scan
   -ps, -prefetch-secrets      prefetch secrets from the secrets file


EXAMPLES:
Run nuclei on single host:
        $ nuclei -target example.com

Run nuclei with specific template directories:
        $ nuclei -target example.com -t http/cves/ -t ssl

Run nuclei against a list of hosts:
        $ nuclei -list hosts.txt

Run nuclei with a JSON output:
        $ nuclei -target example.com -json-export output.json

Run nuclei with sorted Markdown outputs (with environment variables):
        $ MARKDOWN_EXPORT_SORT_MODE=template nuclei -target example.com -markdown-export nuclei_report/

Additional documentation is available at: https://docs.nuclei.sh/getting-started/running
```

<Tip>
  From Nuclei v3.0.0 `-metrics` port has been removed and merged with `-stats`
  when using `-stats` flag metrics will be by default available at `localhost:9092/metrics`
  and metrics-port can be configured by `-metrics-port` flag
</Tip>

### Rate **Limits**

Nuclei have multiple rate limit controls for multiple factors, including a number of templates to execute in parallel, a number of hosts to be scanned in parallel for each template, and the global number of request / per second you wanted to make/limit using nuclei, here is an example of each flag with description.

| Flag       | Description                                                          |
| ---------- | -------------------------------------------------------------------- |
| rate-limit | Control the total number of request to send per seconds              |
| bulk-size  | Control the number of hosts to process in parallel for each template |
| c          | Control the number of templates to process in parallel               |

Feel free to play with these flags to tune your nuclei scan speed and accuracy. For more details on tuning these flag, you can refer [mass-scanning-cli](/opensource/nuclei/mass-scanning-cli)

<Tip>
  `rate-limit` flag takes precedence over the other two flags, the number of
  requests/seconds can't go beyond the value defined for `rate-limit` flag
  regardless the value of `c` and `bulk-size` flag.
</Tip>

### Traffic **Tagging**

Many BugBounty platform/programs requires you to identify the HTTP traffic you make, this can be achieved by setting custom header using config file at `$HOME/.config/nuclei/config.yaml` or CLI flag `-H / header`

<Note>
  Setting custom header using config file

  ```yaml theme={null}
  # Headers to include with each request.
  header:
    - 'X-BugBounty-Hacker: h1/geekboy'
    - 'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) / nuclei'
  ```
</Note>

<Note>
  Setting custom header using CLI flag

  ```yaml theme={null}
  nuclei -header 'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) / nuclei' -list urls.txt -tags cves
  ```
</Note>

### Template **Exclusion**

Nuclei supports a variety of methods for excluding / blocking templates from execution. By default, **nuclei** excludes the tags/templates listed below from execution to avoid unexpected fuzz based scans and some that are not supposed to run for mass scan, and these can be easily overwritten with nuclei configuration file / flags.

Nuclei engine supports two ways to manually exclude templates from scan,

1. Exclude Templates (`-exclude-templates/exclude`)

   **exclude-templates** flag is used to exclude single or multiple templates and directory, multiple `-exclude-templates` flag can be used to provide multiple values.

2. Exclude Tags (`-exclude-tags/etags`)

   **exclude-tags** flag is used to exclude templates based in defined tags, single or multiple can be used to exclude templates.

<Note>
  Example of excluding single template

  ```
  nuclei -list urls.txt -t cves/ -exclude-templates cves/2020/CVE-2020-XXXX.yaml
  ```
</Note>

<Note>
  Example of multiple template exclusion

  ```
  nuclei -list urls.txt -exclude-templates exposed-panels/ -exclude-templates technologies/
  ```
</Note>

<Note>
  Example of excluding templates with single tag

  ```
  nuclei -l urls.txt -t cves/ -etags xss
  ```
</Note>

<Note>
  Example of excluding templates with multiple tags

  ```
  nuclei -l urls.txt -t cves/ -etags sqli,rce
  ```
</Note>

* [.nuclei-ignore](https://github.com/projectdiscovery/nuclei-templates/blob/main/.nuclei-ignore) list - default list of tags and templates excluded from nuclei scan as default.

<Warning>
  **.nuclei-ignore** file is not supposed to be modified by
  user, as it gets used by nuclei internally, to overwrite ignore list, utilize [nuclei
  configuration](/opensource/nuclei/running#nuclei-config) file.
</Warning>

To prioritize certain templates or tags over the [.nuclei-ignore](https://github.com/projectdiscovery/nuclei-templates/blob/master/.nuclei-ignore) file or denylist, you must use the `-include-templates` or `-include-tags` flags. This will ensure that the specified templates or tags take precedence over any `.nuclei-ignore` or denylist entries.

<Note>
  Example of running blocked templates

  ```bash theme={null}
  nuclei -l urls.txt -include-tags iot,misc,fuzz
  ```
</Note>

<Note>
  Example of executing a specific template that is in the denylist

  Say that you have custom templates globbed (`*`) in the denylist on the Nuclei configuration file.

  ```yaml theme={null}
  # ...

  exclude-templates:
    - 'custom/**/*.yaml'
  ```

  But you just want to execute a specific template.

  ```bash theme={null}
  nuclei -l urls.txt -include-templates custom/specific-template.yaml
  ```
</Note>

### List Template Path

`-tl` option in Nuclei is used to list the paths of templates, rather than executing them. This can help you inspect which templates would be used for scan given your current template filter.

```sh theme={null}
# Command to list templates (-tl)
nuclei -tags cve -severity critical,high -author geeknik -tl
```

### Scan on internet database

Nuclei supports integration with [uncover module](https://github.com/projectdiscovery/uncover) that supports services like Shodan, Censys, Hunter, Zoomeye, many more to execute Nuclei on these databases.

Here are uncover options to use -

```console theme={null}
nuclei -h uncover

UNCOVER:
   -uc, -uncover                  enable uncover engine
   -uq, -uncover-query string[]   uncover search query
   -ue, -uncover-engine string[]  uncover search engine (shodan,shodan-idb,fofa,censys,quake,hunter,zoomeye,netlas,criminalip) (default shodan)
   -uf, -uncover-field string     uncover fields to return (ip,port,host) (default "ip:port")
   -ul, -uncover-limit int        uncover results to return (default 100)
   -ucd, -uncover-delay int       delay between uncover query requests in seconds (0 to disable) (default 1)
```

You need to set the API key of the engine you are using as an environment variable in your shell.

```
export SHODAN_API_KEY=xxx
export CENSYS_API_ID=xxx
export CENSYS_API_SECRET=xxx
export FOFA_EMAIL=xxx
export FOFA_KEY=xxx
export QUAKE_TOKEN=xxx
export HUNTER_API_KEY=xxx
export ZOOMEYE_API_KEY=xxx
```

Required API keys can be obtained by signing up on following platform [Shodan](https://account.shodan.io/register), [Censys](https://censys.io/register), [Fofa](https://fofa.info/toLogin), [Quake](https://quake.360.net/quake/#/index), [Hunter](https://user.skyeye.qianxin.com/user/register?next=https%3A//hunter.qianxin.com/api/uLogin\&fromLogin=1) and [ZoomEye](https://www.zoomeye.org/login) .

Example of template execution using a search query.

```
export SHODAN_API_KEY=xxx
nuclei -id 'CVE-2021-26855' -uq 'vuln:CVE-2021-26855' -ue shodan
```

It can also read queries from templates metadata and execute template against hosts returned by uncover for that query.

Example of template execution using template-defined search queries.

Template snippet of [CVE-2021-26855](https://github.com/projectdiscovery/nuclei-templates/blob/master/cves/2021/CVE-2021-26855.yaml)

```yaml theme={null}
metadata:
  shodan-query: 'vuln:CVE-2021-26855'
```

```console theme={null}
nuclei -t cves/2021/CVE-2021-26855.yaml -uncover
nuclei -tags cve -uncover
```

We can update the nuclei configuration file to include these tags for all scans.

## Nuclei **Config**

> Since release of [v2.3.2](https://blog.projectdiscovery.io/nuclei-v2-3-0-release/) nuclei uses [goflags](https://github.com/projectdiscovery/goflags) for clean CLI experience and long/short formatted flags.
>
> [goflags](https://github.com/projectdiscovery/goflags) comes with auto-generated config file support that coverts all available CLI flags into config file, basically you can define all CLI flags into config file to avoid repetitive CLI flags that loads as default for every scan of nuclei.
>
> Default path of nuclei config file is `$HOME/.config/nuclei/config.yaml`, uncomment and configure the flags you wish to run as default.

Here is an example config file:

```yaml theme={null}
# Headers to include with all HTTP request
header:
  - 'X-BugBounty-Hacker: h1/geekboy'

# Directory based template execution
templates:
  - cves/
  - vulnerabilities/
  - misconfiguration/

# Tags based template execution
tags: exposures,cve

# Template Filters
tags: exposures,cve
author: geeknik,pikpikcu,dhiyaneshdk
severity: critical,high,medium

# Template Allowlist
# 
# Note: This will take precedence over the .nuclei-ignore file and denylist
# entries (exclude-tags or exclude-templates list).
include-tags: dos,fuzz # Tag based inclusion
include-templates: # Template based inclusion
  - vulnerabilities/xxx
  - misconfiguration/xxxx

# Template Denylist
exclude-tags: info # Tag based exclusion
exclude-templates: # Template based exclusion
  - vulnerabilities/xxx
  - misconfiguration/xxxx

# Rate Limit configuration
rate-limit: 500
bulk-size: 50
concurrency: 50
```

Once configured, **the config file will be used by default**, additional custom config files can also be provided using multiple `-config` flags.

<Note>
  **Running nuclei with custom config file**

  ```
  nuclei -config project.yaml -list urls.txt
  ```
</Note>

## Nuclei Result Dashboard

Nuclei now allows seamless integration with the ProjectDiscovery Cloud Platform to simplify the visualization of Nuclei results and generate swift reports. This highly requested feature from the community enables easier handling of scan results with minimal effort.

Follow the steps below to set up your PDCP Result Dashboard:

1. Visit [https://cloud.projectdiscovery.io](https://cloud.projectdiscovery.io) to create free PDCP API key.

<img class="block" src="https://mintcdn.com/projectdiscovery/PrBSST-qkD3tzRi-/images/pdcp-api-key.png?fit=max&auto=format&n=PrBSST-qkD3tzRi-&q=85&s=4b4da5284cadf438603e461ad3ef0fe3" alt="PDCP API Key" width="2654" height="1078" data-path="images/pdcp-api-key.png" />

2. Use the `nuclei -auth` command, enter your API key when prompted.
3. To perform a scan and upload the results straight to the cloud, use the `-cloud-upload` option while running a nuclei scan.

An example command might look like this:

```bash theme={null}
nuclei -target http://honey.scanme.sh -cloud-upload
```

And the output would be like this:

```console theme={null}
                     __     _
   ____  __  _______/ /__  (_)
  / __ \/ / / / ___/ / _ \/ /
 / / / / /_/ / /__/ /  __/ /
/_/ /_/\__,_/\___/_/\___/_/   v3.1.0

      projectdiscovery.io

[INF] Current nuclei version: v3.1.0 (latest)
[INF] Current nuclei-templates version: v9.6.9 (latest)
[INF] To view results on cloud dashboard, visit https://cloud.projectdiscovery.io/scans upon scan completion.
[INF] New templates added in latest release: 73
[INF] Templates loaded for current scan: 71
[INF] Executing 71 signed templates from projectdiscovery/nuclei-templates
[INF] Targets loaded for current scan: 1
[INF] Using Interactsh Server: oast.live
[CVE-2017-9506] [http] [medium] http://honey.scanme.sh/plugins/servlet/oauth/users/icon-uri?consumerUri=http://clk37fcdiuf176s376hgjzo3xsoq5bdad.oast.live
[CVE-2019-9978] [http] [medium] http://honey.scanme.sh/wp-admin/admin-post.php?swp_debug=load_options&swp_url=http://clk37fcdiuf176s376hgyk9ppdqe9a83z.oast.live
[CVE-2019-8451] [http] [medium] http://honey.scanme.sh/plugins/servlet/gadgets/makeRequest
[CVE-2015-8813] [http] [high] http://honey.scanme.sh/Umbraco/feedproxy.aspx?url=http://clk37fcdiuf176s376hgj885caqoc713k.oast.live
[CVE-2020-24148] [http] [critical] http://honey.scanme.sh/wp-admin/admin-ajax.php?action=moove_read_xml
[CVE-2020-5775] [http] [medium] http://honey.scanme.sh/external_content/retrieve/oembed?endpoint=http://clk37fcdiuf176s376hgyyxa48ih7jep5.oast.live&url=foo
[CVE-2020-7796] [http] [critical] http://honey.scanme.sh/zimlet/com_zimbra_webex/httpPost.jsp?companyId=http://clk37fcdiuf176s376hgi9b8sd33se5sr.oast.live%23
[CVE-2017-18638] [http] [high] http://honey.scanme.sh/composer/send_email?to=hVsp@XOvw&url=http://clk37fcdiuf176s376hgyf8y81i9oju3e.oast.live
[CVE-2018-15517] [http] [high] http://honey.scanme.sh/index.php/System/MailConnect/host/clk37fcdiuf176s376hgi5j3fsht3dchj.oast.live/port/80/secure/
[CVE-2021-45967] [http] [critical] http://honey.scanme.sh/services/pluginscript/..;/..;/..;/getFavicon?host=clk37fcdiuf176s376hgh1y3xjzb3yjpy.oast.live
[CVE-2021-26855] [http] [critical] http://honey.scanme.sh/owa/auth/x.js
[INF] Scan results uploaded! View them at https://cloud.projectdiscovery.io/scans/clk37krsr14s73afc3ag
```

After the scan, a URL will be displayed on the command line interface. Visit this URL to check your results on the Cloud Dashboard.

<img src="https://mintcdn.com/projectdiscovery/PrBSST-qkD3tzRi-/images/pdcp-result-dashboard.png?fit=max&auto=format&n=PrBSST-qkD3tzRi-&q=85&s=0a64389aca0cf5b08cdeaaa581d3a97a" alt="PDCP Result Dashboard" width="4064" height="2176" data-path="images/pdcp-result-dashboard.png" />

### Advanced Integration Options

**Setting API key via environment variable**

Avoid entering your API key via interactive prompt by setting it via environment variable.

```sh theme={null}
export PDCP_API_KEY=XXXX-XXXX
```

**Enabling result upload by default**

If you want all your scans to automatically upload results to the cloud, enable the `ENABLE_CLOUD_UPLOAD` environment variable.

```sh theme={null}
export ENABLE_CLOUD_UPLOAD=true
```

**Disabling cloud upload warnings**

To suppress warnings about result uploads, disable the `DISABLE_CLOUD_UPLOAD_WRN` environment variable.

```sh theme={null}
export DISABLE_CLOUD_UPLOAD_WRN=true
```

Your configured PDCP API key stored in `$HOME/.pdcp/credentials.yaml`

<Warning>
  Nuclei OSS results uploaded to the cloud platform are scheduled for automatic cleanup after 30 days, although this duration is subject to change as we gauge user feedback and requirement.
</Warning>

## Nuclei Reporting

Nuclei comes with reporting module support with the release of v2.3.0 supporting GitHub, GitLab, and Jira integration, this allows nuclei engine to create automatic tickets on the supported platform based on found results.

| Platform | GitHub | GitLab | Jira | Markdown | SARIF | Elasticsearch | Splunk HEC | MongoDB |
| -------- | :----: | :----: | :--: | :------: | :---: | :-----------: | :--------: | :-----: |
| Support  |    ✔   |    ✔   |   ✔  |     ✔    |   ✔   |       ✔       |      ✔     |    ✔    |

`-rc, -report-config` flag can be used to provide a config file to read configuration details of the platform to integrate. Here is an [example config file](https://github.com/projectdiscovery/nuclei/blob/main/cmd/nuclei/issue-tracker-config.yaml) for all supported platforms.

For example, to create tickets on GitHub, create a config file with the following content and replace the appropriate values:

```yaml theme={null}
# GitHub contains configuration options for GitHub issue tracker

github:
  username: '$user'
  owner: '$user'
  token: '$token'
  project-name: 'testing-project'
  issue-label: 'Nuclei'
  duplicate-issue-check: true
```

Alternatively if you use GitLab, create a config file following content and replace the appropriate values:

```yaml theme={null}
# GitLab contains configuration options for GitLab issue tracker

gitlab:
  username: '$user'
  base-url: 'gitlab.com'
  token: '$token'
  project-name: 'testing-project'
  issue-label: 'nuclei-label'
  severity-as-label: true
  duplicate-issue-check: true
```

To store results in Elasticsearch, create a config file with the following content and replace the appropriate values:

```yaml theme={null}
# elasticsearch contains configuration options for elasticsearch exporter
elasticsearch:
  # IP for elasticsearch instance
  ip: 127.0.0.1
  # Port is the port of elasticsearch instance
  port: 9200
  # IndexName is the name of the elasticsearch index
  index-name: nuclei
```

To forward results to Splunk HEC, create a config file with the following content and replace the appropriate values:

```yaml theme={null}
# splunkhec contains configuration options for splunkhec exporter
splunkhec:
  # Hostname for splunkhec instance
  host: '$hec_host'
  # Port is the port of splunkhec instance
  port: 8088
  # IndexName is the name of the splunkhec index
  index-name: nuclei
  # SSL enables ssl for splunkhec connection
  ssl: true
  # SSLVerification disables SSL verification for splunkhec
  ssl-verification: true
  # HEC Token for the splunkhec instance
  token: '$hec_token'
```

To forward results to Jira, create a config file with the following content and replace the appropriate values:

The Jira reporting options allows for custom fields, as well as using variables from the Nuclei templates in those custom fields.
The supported variables currently are: `$CVSSMetrics`, `$CVEID`, `$CWEID`, `$Host`, `$Severity`, `$CVSSScore`, `$Name`

In addition, Jira is strict when it comes to custom field entry. If the field is a dropdown, Jira accepts only the case sensitive specific string and the API call is slightly different. To support this, there are three types of customfields.

* `name` is the dropdown value
* `id` is the ID value of the dropdown
* `freeform` is if the customfield the entry of any value

To avoid duplication, the JQL query run can be slightly modified by the config file.
The `CLOSED_STATUS` can be changed in the Jira template file using the `status-not` variable.
`summary ~ TEMPLATE_NAME AND summary ~ HOSTNAME AND status != CLOSED_STATUS`

```yaml theme={null}
jira:
  # cloud is the boolean which tells if Jira instance is running in the cloud or on-prem version is used
  cloud: true
  # update-existing is the boolean which tells if the existing, opened issue should be updated or new one should be created
  update-existing: false
  # URL is the jira application url
  url: https://localhost/jira
  # account-id is the account-id of the Jira user or username in case of on-prem Jira
  account-id: test-account-id
  # email is the email of the user for Jira instance
  email: test@test.com
  # token is the token for Jira instance or password in case of on-prem Jira
  token: test-token
  #project-name is the name of the project.
  project-name: test-project-name
  #issue-type is the name of the created issue type (case sensitive)
  issue-type: Bug
  # SeverityAsLabel (optional) sends the severity as the label of the created issue
  # User custom fields for Jira Cloud instead
  severity-as-label: true
  # Whatever your final status is that you want to use as a closed ticket - Closed, Done, Remediated, etc
  # When checking for duplicates, the JQL query will filter out status's that match this.
  # If it finds a match _and_ the ticket does have this status, a new one will be created.
  status-not: Closed
  # Customfield supports name, id and freeform. name and id are to be used when the custom field is a dropdown.
  # freeform can be used if the custom field is just a text entry
  # Variables can be used to pull various pieces of data from the finding itself.
  # Supported variables: $CVSSMetrics, $CVEID, $CWEID, $Host, $Severity, $CVSSScore, $Name
  custom_fields:
    customfield_00001:
      name: 'Nuclei'
    customfield_00002:
      freeform: $CVSSMetrics
    customfield_00003:
      freeform: $CVSSScore
```

To write results to a MongoDB database collection, update the config file with the connection information.

```yaml theme={null}
mongodb:
  # the connection string to the MongoDB database
  # (e.g., mongodb://root:example@localhost:27017/nuclei?ssl=false&authSource=admin)
  connection-string: ""
  # the name of the collection to store the issues
  collection-name: ""
  # excludes the Request and Response from the results (helps with filesize)
  omit-raw: false
  # determines the number of results to be kept in memory before writing it to the database or 0 to
  # persist all in memory and write all results at the end (default)
  batch-size: 0
```

**Running nuclei with reporting module:**

```bash theme={null}
nuclei -l urls.txt -t cves/ -rc issue-tracker.yaml
```

Similarly, other platforms can be configured. Reporting module also supports basic filtering and duplicate checks to avoid duplicate ticket creation.

```yaml theme={null}
allow-list:
  severity: high,critical
```

This will ensure to only creating tickets for issues identified with **high** and **critical** severity; similarly, `deny-list` can be used to exclude issues with a specific severity.

If you are running periodic scans on the same assets, you might want to consider `-rdb, -report-db` flag that creates a local copy of the valid findings in the given directory utilized by reporting module to compare and **create tickets for unique issues only**.

```bash theme={null}
nuclei -l urls.txt -t cves/ -rc issue-tracker.yaml -rdb prod
```

**<ins>Markdown Export</ins>**

Nuclei supports markdown export of valid findings with `-me, -markdown-export` flag, this flag takes directory as input to store markdown formatted reports.

Including request/response in the markdown report is optional, and included when `-irr, -include-rr` flag is used along with `-me`.

```bash theme={null}
nuclei -l urls.txt -t cves/ -irr -markdown-export reports
```

**<ins>SARIF Export</ins>**

Nuclei supports SARIF export of valid findings with `-se, -sarif-export` flag. This flag takes a file as input to store SARIF formatted report.

```bash theme={null}
nuclei -l urls.txt -t cves/ -sarif-export report.sarif
```

It is also possible to visualize Nuclei results using **SARIF** files.

1. By uploading a SARIF file to [SARIF Viewer](https://microsoft.github.io/sarif-web-component/)

2. By uploading a SARIF file to [Github Actions](https://docs.github.com/en/code-security/code-scanning/integrating-with-code-scanning/uploading-a-sarif-file-to-github)

More info on the SARIF output is documented [here](https://github.com/projectdiscovery/nuclei/pull/2925).

<Note>
  These are **not official** viewers of Nuclei and `Nuclei` has no liability
  towards any of these options to visualize **Nuclei** results. These are just
  some publicly available options to visualize SARIF files.
</Note>

## Scan **Metrics**

Nuclei expose running scan metrics on a local port `9092` when `-metrics` flag is used and can be accessed at **localhost:9092/metrics**, default port to expose scan information is configurable using `-metrics-port` flag.

Here is an example to query `metrics` while running nuclei as following `nuclei -t cves/ -l urls.txt -metrics`

```bash theme={null}
curl -s localhost:9092/metrics | jq .
```

```json theme={null}
{
  "duration": "0:00:03",
  "errors": "2",
  "hosts": "1",
  "matched": "0",
  "percent": "99",
  "requests": "350",
  "rps": "132",
  "startedAt": "2021-03-27T18:02:18.886745+05:30",
  "templates": "256",
  "total": "352"
}
```

## Passive Scan

Nuclei engine supports passive mode scanning for HTTP based template utilizing file support, with this support we can run HTTP based templates against locally stored HTTP response data collected from any other tool.

```sh theme={null}
nuclei -passive -target http_data
```

<Note>Passive mode support is limited for templates having `{{BasedURL}}` or `{{BasedURL/}}` as base path.</Note>

## Running With Docker

If Nuclei was installed within a Docker container based on the [installation instructions](./install),
the executable does not have the context of the host machine. This means that the executable will not be able to access
local files such as those used for input lists or templates. To resolve this, the container should be run with volumes
mapped to the local filesystem to allow access to these files.

### Basic Usage

This example runs a Nuclei container against `google.com`, prints the results to JSON and removes the container once it
has completed:

```sh theme={null}
docker run --rm projectdiscovery/nuclei -u google.com -jsonl
```

### Using Volumes

This example runs a Nuclei container against a list of URLs, writes the results to a `.jsonl` file and removes the
container once it has completed.

```sh theme={null}
# This assumes there's a file called `urls.txt` in the current directory
docker run --rm -v ./:/app/ projectdiscovery/nuclei -l /app/urls.txt -jsonl /app/results.jsonl
# The results will be written to `./results.jsonl` on the host machine once the container has completed
```

======================================================================
## VERBATIM DOC: templates_faq.md
======================================================================
> ## Documentation Index
> Fetch the complete documentation index at: https://docs.projectdiscovery.io/llms.txt
> Use this file to discover all available pages before exploring further.

# Nuclei Templates FAQ

> Common questions and answers about Nuclei templates, including usage tips and best practices.

<Tip>For info on the Nuclei Template Editor or using templates on our cloud platform - [learn more here](/cloud/editor/overview).</Tip>

<AccordionGroup>
  <Accordion title="What are Nuclei templates?" icon="circle-info" iconType="solid">
    Nuclei [templates](http://github.com/projectdiscovery/nuclei-templates) are the core of the Nuclei project. The templates contain the actual logic that is executed in order to detect various vulnerabilities. The project consists of **several thousand** ready-to-use **[community-contributed](https://github.com/projectdiscovery/nuclei-templates/graphs/contributors)** vulnerability templates.
  </Accordion>

  <Accordion title="How can I write Nuclei templates?" icon="circle-info" iconType="solid">
    We maintain a [template guide](/templates/introduction/) for writing new and custom Nuclei templates.
  </Accordion>

  <Accordion title="How can writing Nuclei templates help me or my organization?" icon="fire-flame-curved" iconType="solid">
    Performing security assessment of an application is time-consuming. It's always better and time-saving to automate steps whenever possible. Once you've found a security vulnerability, you can prepare a Nuclei template by defining the required HTTP request to reproduce the issue, and test the same vulnerability across multiple hosts with ease. It's worth mentioning ==you write the template once and use it forever==, as you don't need to manually test that specific vulnerability any longer.

    Here are few examples from the community making use of templates to automate the security findings:

    * [https://dhiyaneshgeek.github.io/web/security/2021/02/19/exploiting-out-of-band-xxe/](https://dhiyaneshgeek.github.io/web/security/2021/02/19/exploiting-out-of-band-xxe/)
      * [https://blog.melbadry9.xyz/fuzzing/nuclei-cache-poisoning](https://blog.melbadry9.xyz/fuzzing/nuclei-cache-poisoning)
      * [https://blog.melbadry9.xyz/dangling-dns/xyz-services/ddns-worksites](https://blog.melbadry9.xyz/dangling-dns/xyz-services/ddns-worksites)
      * [https://blog.melbadry9.xyz/dangling-dns/aws/ddns-ec2-current-state](https://blog.melbadry9.xyz/dangling-dns/aws/ddns-ec2-current-state)
      * [https://projectdiscovery.io/blog/if-youre-not-writing-custom-nuclei-templates-youre-missing-out](https://projectdiscovery.io/blog/if-youre-not-writing-custom-nuclei-templates-youre-missing-out)
  </Accordion>

  <Accordion title="How do I run Nuclei templates?" icon="circle-info" iconType="solid">
    Nuclei templates can be executed using a template name or with tags, using `-templates` (`-t`) and `-tags` flag, respectively.

    ```
    nuclei -tags cve -list target_urls.txt
    ```
  </Accordion>

  <Accordion title="How can I contribute a Nuclei template?" icon="circle-info" iconType="solid">
    You are always welcome to share your templates with the community. You can either open a [GitHub issue](https://github.com/projectdiscovery/nuclei-templates/issues/new?assignees=\&labels=nuclei-template\&template=submit-template.md\&title=%5Bnuclei-template%5D+template-name) with the template details or open a GitHub [pull request](https://github.com/projectdiscovery/nuclei-templates/pulls) with your nuclei templates. If you don't have a GitHub account, you can also make use of the [discord server](https://discord.gg/projectdiscovery) to share the template with us.
  </Accordion>

  <Accordion title="I'm getting false-positive results!" icon="triangle-exclamation" iconType="solid">
    The Nuclei template project is a **community-contributed project**. The ProjectDiscovery team manually reviews templates before merging them into the project. Still, there is a possibility that some templates with weak matchers will slip through the verification. This could produce false-positive results. **Templates are only as good as their matchers.**

    If you identified templates producing false positive/negative results, here are few steps that you can follow to fix them quickly.

    <Accordion title="I found a template producing false positive or negative results, but I'm not sure if this is accurate." icon="circle-info" iconType="solid">
      Direct message us on [Twitter](https://twitter.com/pdnuclei) or [Discord](https://discord.gg/projectdiscovery) to confirm the validity of the template.
    </Accordion>

    <Accordion title="I found a template producing false positive or negative result and I don't know how to fix it." icon="circle-info" iconType="solid">
      Please open a GitHub [issue](https://github.com/projectdiscovery/nuclei-templates/issues/new?assignees=\&labels=false-positive\&template=false-positive.md\&title=%5Bfalse-positive%5D+template-name+) with details, and we will work to address the problem and update the template.
    </Accordion>

    <Accordion title="I found a template producing a false positive or negative result and I know how to fix it." icon="circle-info" iconType="solid">
      Please open a GitHub [pull request](https://github.com/projectdiscovery/nuclei-templates/pulls) with fix.
    </Accordion>
  </Accordion>

  <Accordion title="Why can't I run all Nuclei templates?" icon="triangle-exclamation" iconType="solid">
    The Nuclei templates project houses a variety of templates which perform fuzzing and other actions which may result in a DoS against the target system (see [the list here](https://github.com/projectdiscovery/nuclei-templates/blob/master/.nuclei-ignore)). To ensure  these templates are not accidentally run, they are tagged and excluded them from the default scan. These templates can be only executed when explicitly invoked using the `-itags` option.
  </Accordion>

  {" "}

  <Accordion title="Templates exist on GitHub but are not running with Nuclei?" icon="triangle-exclamation" iconType="solid">
    When you download or update Nuclei templates using the Nuclei binary, it
    downloads all the templates from the latest **release**. All templates added
    after the release exist in the [master
    branch](https://github.com/projectdiscovery/nuclei-templates) and are added to
    Nuclei when a new template release is created.
  </Accordion>
</AccordionGroup>
