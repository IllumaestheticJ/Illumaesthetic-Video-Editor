"""Pick the Cycles render device: GPU when the machine has one, else CPU.

    import ive_gpu; ive_gpu.use(bpy.context.scene)

- GPU machines (e.g. the RTX 3060 Ti worker): OptiX first, then CUDA/HIP/Metal/oneAPI. Only the GPU
  devices are enabled. Mixing the CPU in sends OIDN denoising to the CPU, which made a 1080x1920 /
  32 spp frame 4x slower (5.8 s vs 1.4 s), so the CPU is left out and denoising runs on the GPU.
- Cloud machines with no GPU: unchanged, Cycles CPU.
- IVE_DEVICE=CPU forces the CPU (e.g. to compare a frame against an older CPU render).
Prints one 'IVE_DEVICE ...' line so render logs show which device was used.
"""
import os

import bpy


def use(sc=None):
    sc = sc or bpy.context.scene
    sc.cycles.device = "CPU"
    if os.environ.get("IVE_DEVICE", "").upper() == "CPU":
        print("IVE_DEVICE CPU (forced by IVE_DEVICE)")
        return "CPU"
    try:
        prefs = bpy.context.preferences.addons["cycles"].preferences
    except Exception:
        print("IVE_DEVICE CPU (no cycles prefs)")
        return "CPU"
    for kind in ("OPTIX", "CUDA", "HIP", "METAL", "ONEAPI"):
        try:
            prefs.compute_device_type = kind
            prefs.get_devices()
        except (TypeError, ValueError):
            continue
        gpus = [d for d in prefs.devices if d.type == kind]
        if not gpus:
            continue
        for d in prefs.devices:
            d.use = d.type == kind
        sc.cycles.device = "GPU"
        try:
            sc.cycles.denoising_use_gpu = True
        except AttributeError:
            pass
        print("IVE_DEVICE GPU", kind, ", ".join(d.name for d in gpus))
        return kind
    print("IVE_DEVICE CPU (no GPU found)")
    return "CPU"


if __name__ == "__main__":  # `blender -b x.blend -P blender/ive_gpu.py -a` picks the device for the loaded scene
    use()
