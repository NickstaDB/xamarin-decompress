# xamarin-decompress
Decompress Xamarin .NET compressed binaries so they can be decompiled.

This pull request on the xamarin-android project implemented compression for .NET assemblies inside Android `.apk` files: [https://github.com/xamarin/xamarin-android/pull/4686](https://github.com/xamarin/xamarin-android/pull/4686). This prevents those assemblies from being decompiled until they have been decompressed, which is where this script comes in.

The script checks for the `XALZ` header which indicates a compressed assembly and decompresses it using LZ4 block decompression so that the resulting file can be decompiled using your tool of choice.

## Usage
To decompress a single file run the script as follows:

```
python3 xamarin-decompress.py target-assembly.dll
```

This will generate `target-assembly.decompressed.dll` which can be decompiled. To overwrite the original assembly file with the decompressed one, pass the `-o` flag e.g.

```
python3 xamarin-decompress.py -o target-assembly.dll
```

To scan a directory for all Xamarin .NET compressed `.dll` and `.exe` files, run the script as follows:

```
python3 xamarin-decompress.py dir-where-you-extracted-the-apk
```

Likewise, the `-o` flag can be used to replace the original files.
