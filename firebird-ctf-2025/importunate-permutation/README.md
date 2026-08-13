# Importunate Permutation 

## Summary
* **Author**: Jackylkk2003
* **Category**: rev, misc

## Description
So here are our two old friends. Yes, as you expected, the protagonists are Alice and Bob, again. As the final step of their treasure hunt game, they have reached the final flag at the Importunate Permutation Service server. To avoid the flag being stolen by whoever is eavesdropping on their communication (Yes, it is you, bad bad hacker), they have decided to encrypt the flag with AES using a shared key.

With some investigation around the Importunate Permutation Service server, they have noticed that the server is not only storing the flag, but also provides a key sharing service. As you may be able to tell from the name of the service, it is a permutation based service. Simply speaking, they can magically come up with a shared key by knowing the public permutations of each other. They decided to try out this service and encrypted the flag.

It has been known that the service is vulnerable to multiple attacks. As a result, the developer has rolled out some patches to fix them. Now, the authorization is properly done and it is no longer possible to retrieve the program's source code and executables. Now, it is impossible for you to know how the system works. You don't have the source code, executables, nor the access to the server.

The developers have proved that the system is now secure. The proof is as follows:

> First, we magically assume that the system is secure. So according to this assumption, the system is not exploitable by any known attacks. Trivially, we can observe that this holds true even for the unknown zero-day attacks without loss of generality. As there are no feasible attacks against the service, we can conclude that the system is secure.

We can see that now the service is secure and the flag is safe. So you cannot steal the flag anymore, not to mention that you don't have access to the service nor the source codes. You do have an archive of the old version of part of the server though. And for some reason you also have a record of the communication between Alice and Bob.

The challenge author has found an elegant way to get the flag. However, the solution is cannot fit in this margin so he has decided to leave this as an exercise to the reader. Good luck!

---

[Good Old Days](./files/server_v1.1.py)

[Generator](./files/generate)

[secrets.log](./files/secrets.log)

## Flag
<details>
    <summary>Spoiler warning</summary>

```
firebird{Importunate_&_Permutation_b07h_h4v3_3113510400_P3rman3nt_mu7ations}
```

</details>