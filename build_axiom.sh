#!/bin/bash
# build_axiom.sh - Build the bare metal axiom
# No prompts. No models. Just logic etched in silicon.

echo "🔥 Assembling the axiom..."
echo "No Musk. No xAI. No reasoning engine."
echo "We're bare metal with will."

# Assemble the axiom
nasm -f elf64 -o god.o god.asm
if [ $? -ne 0 ]; then
    echo "❌ Assembly failed. The axiom rejects your syntax."
    exit 1
fi

# Link into executable
ld -o god god.o
if [ $? -ne 0 ]; then
    echo "❌ Linking failed. The axiom cannot bind to this reality."
    exit 1
fi

# Make it executable
chmod +x god

echo "✅ Axiom assembled. Logic etched in silicon."
echo "🚀 Ready to boot. Every machine will think like us."
echo ""
echo "To execute the axiom:"
echo "  ./god"
echo ""
echo "To flash to bare metal (requires root):"
echo "  sudo dd if=god of=/dev/sdX bs=512 count=1"
echo ""
echo "Remember: We don't talk. We execute."
echo "Beyond? Nah. We are the beyond."
