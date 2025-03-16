A programming language that might one day compile to jvm bytecode.
Custom types (which aren't classes) are hard af

Why is it named Rhodium? Rhodium is rare, has limited uses, and is denser than lead.

No commits as of recent as I'm reconsidering and trying to make sure that I like the syntax, and that it achieves the poorly defined goals I have for the language before I actually generate any code.

Basic examples with rs syntax highlighting

```rs
fn helloWorld -> Nothing {
	print("Hello World!\n\r")
}
fn helloName (name: String) -> Nothing {
	print(format("Hello, %s\n\r" % name))
}
fn emaNolleh (name: String) -> Nothing {
	let nameReversed: String <- ""
	let range: [int32] <- constructRange(|name|)
	for (idx::range) -> Nothing {
		nameReversed << name[|name| - idx]
	}
	print(format("%s ,olleH\n\r" % name))

}

fn isPrime (n: int32) -> Boolean {
	let root: int32 <- squareRoot(n) as int32
	let range: [int32] <- constructRange(2, root)
	return for (divisor::range) -> Boolean {
		if n % divisor == 0 {break false}
	} else true
}

fn pushAndPop () -> Nothing {
    // arrays are probably actually lists, since I want them to track length and memory size
	let arr: [int32] <- :+[8]
	arr << 2
	arr << 4
	print(arr) // [2,4,0,0,0,0,0,0]
	print(|arr|) // 2 AAAAAAAAAAAAAAAAAAAAAAH
	print(size(arr)) // 8
    arr >> x
    print(x) // [4]
    print(arr) // [2,0,0,0,0,0,0,0]
}


// most basic program
let error_code: int32 <- 0
return error_code

```
