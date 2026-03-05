def synthesize_findings(parameters, interpretations, risks, recommendations):
    """
    Combines outputs from multiple AI models
    into a single human-readable summary with proper formatting.
    """

    summary = []

    if not parameters:
        return "No clinical data could be extracted from the report."

    # Enhanced header with analysis info
    summary.append("═" * 70)
    summary.append("📋 COMPREHENSIVE HEALTH ANALYSIS REPORT")
    summary.append("═" * 70)

    # Section 1: Extracted Parameters with Clinical Context
    if parameters:
        summary.append("\n🔬 EXTRACTED CLINICAL PARAMETERS:")
        summary.append("─" * 70)
        param_count = len(parameters)
        if param_count > 0:
            summary.append(f"Total Parameters Analyzed: {param_count}")
            summary.append("")
            
            for i, (k, v) in enumerate(parameters.items(), 1):
                # Format parameter name and value
                param_name = str(k).replace("_", " ").title()
                try:
                    # Try to format numbers with appropriate precision
                    if isinstance(v, (int, float)):
                        formatted_val = f"{float(v):.2f}" if isinstance(v, float) else str(v)
                    else:
                        formatted_val = str(v)
                    summary.append(f"  {i:2d}. {param_name:30s} : {formatted_val}")
                except:
                    summary.append(f"  {i:2d}. {param_name:30s} : {v}")

    # Section 2: Clinical Interpretations (sorted by importance)
    if interpretations:
        summary.append("\n\n🧠 CLINICAL INTERPRETATION:")
        summary.append("─" * 70)
        summary.append("Analysis of blood parameters and their clinical significance:")
        summary.append("")
        for i, interp in enumerate(interpretations, 1):
            # Add emoji for severity if not present
            interp_str = str(interp)
            if "abnormal" in interp_str.lower() or "high" in interp_str.lower() or "low" in interp_str.lower():
                emoji = "⚠️"
            elif "normal" in interp_str.lower() or "healthy" in interp_str.lower():
                emoji = "✅"
            else:
                emoji = "📌"
            summary.append(f"  {i}. {emoji} {interp_str}")

    # Section 3: Identified Risks (sorted by severity)
    if risks:
        summary.append("\n\n⚠️  IDENTIFIED HEALTH RISKS:")
        summary.append("─" * 70)
        summary.append("Potential health concerns that require attention:")
        summary.append("")
        for i, risk in enumerate(risks, 1):
            risk_str = str(risk)
            # Add severity indicator
            if "critical" in risk_str.lower() or "severe" in risk_str.lower():
                severity = "🔴 CRITICAL"
            elif "high" in risk_str.lower():
                severity = "🟠 HIGH"
            elif "moderate" in risk_str.lower():
                severity = "🟡 MODERATE"
            else:
                severity = "🟢 LOW"
            summary.append(f"  {i}. [{severity}] {risk_str}")

    # Section 4: Recommendations (sorted by priority)
    if recommendations:
        summary.append("\n\n💡 RECOMMENDED ACTIONS:")
        summary.append("─" * 70)
        summary.append("Actionable recommendations based on analysis:")
        summary.append("")
        for i, rec in enumerate(recommendations, 1):
            rec_str = str(rec)
            # Add priority indicator
            if "immediate" in rec_str.lower() or "urgent" in rec_str.lower():
                priority = "🔴 URGENT"
            elif "consult" in rec_str.lower() or "doctor" in rec_str.lower() or "provider" in rec_str.lower():
                priority = "🟠 IMPORTANT"
            else:
                priority = "🟢 ROUTINE"
            summary.append(f"  {i}. [{priority}] {rec_str}")

    # Footer
    summary.append("\n" + "═" * 70)
    summary.append("📌 DISCLAIMER: This is an AI-assisted analysis for informational purposes.")
    summary.append("Please consult a healthcare professional for personalized medical advice.")
    summary.append("═" * 70)

    return "\n".join(summary)
