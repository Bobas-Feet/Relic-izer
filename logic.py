# import tkinter as tk
# from tkinter import ttk, messagebox
# from lists_database import character_names  # if needed
#
# calculation_history = []
#
#
# def summarize_all():
#
#     text_output.delete(1.0, tk.END)
#
#     if not validate_inputs():
#         print_output("Something's missing. Either it's Current Relic, Target Relic, or both.")
#         return
#
#     if not calculation_history:
#         print_output("Before calculation, you'll need to add to the queue at least one line, genius.")
#         return
#
#     total_salvage = [0] * len(Salvage)
#     total_signal = [0] * len(Signal_Data)
#     output_lines = ["                          === INDIVIDUAL SUMMARY ===\n"]
#
#     for i, (name, current, target) in enumerate(calculation_history, 1):
#         label = f"{name}" if name else f"Upgrade #{i}"
#         output_lines.append(f"=== {label} ===")
#         salvage_diff, signal_diff = calculate_mats_sum(current, target)
#         output_lines.append(f" - Relic {current} → Relic {target} - ")
#
#         # Only show "Salvage" section if there's data
#         if any(amount > 0 for amount in salvage_diff):
#             output_lines.append("Salvage")
#             for s_name, amount in zip(Salvage, salvage_diff):
#                 if amount > 0:
#                     output_lines.append(f"   - {s_name}: {amount}")
#
#         # Only show "Signal Data" section if there's data
#         if any(amount > 0 for amount in signal_diff):
#             output_lines.append("Signal Data")
#             for sig_name, amount in zip(Signal_Data, signal_diff):
#                 if amount > 0:
#                     output_lines.append(f"   - {sig_name}: {amount}")
#
#         output_lines.append("")
#
#         total_salvage = [x + y for x, y in zip(total_salvage, salvage_diff)]
#         total_signal = [x + y for x, y in zip(total_signal, signal_diff)]
#
#     # Only append GRAND TOTAL if there is more than one line in the queue
#     if len(calculation_history) > 1:
#         output_lines.append("                               === GRAND TOTAL ===\n")
#
#         # Only show total salvage if there is any salvage data
#         if any(amount > 0 for amount in total_salvage):
#             output_lines.append("Salvage")
#             for s_name, amount in zip(Salvage, total_salvage):
#                 if amount > 0:
#                     output_lines.append(f"   - {s_name}s: {amount} pieces")
#
#         # Only show total signal data if there is any signal data
#         if any(amount > 0 for amount in total_signal):
#             output_lines.append("Signal Data")
#             for sig_name, amount in zip(Signal_Data, total_signal):
#                 if amount > 0:
#                     output_lines.append(f"   - {sig_name}: {amount}")
#         output_lines.append("")
#
#     print_output("\n".join(output_lines))
#     text_output.yview_moveto(0.0)
#
#
# def validate_inputs():
#     valid = True
#
#     try:
#         current = int(current_entry.get())
#     except ValueError:
#         current = None
#     try:
#         target = int(target_entry.get())
#     except ValueError:
#         target = None
#
#     # Reset to default border
#     current_frame.config(highlightbackground="SystemButtonFace")
#     target_frame.config(highlightbackground="SystemButtonFace")
#
#     if current is None or not (0 <= current <= 8):
#         current_frame.config(highlightbackground="red")
#         valid = False
#
#     if target is None or not (1 <= target <= 9):
#         target_frame.config(highlightbackground="red")
#         valid = False
#
#     if current is not None and target is not None and current >= target:
#         current_frame.config(highlightbackground="red")
#         target_frame.config(highlightbackground="red")
#         valid = False
#
#     return valid
#
#
# def calculate_mats_sum(current_relic, target_relic):
#
#     total_salvage_dif = [0] * len(Salvage)
#     total_signalData_dif = [0] * len(Signal_Data)
#     for relic_level in range(current_relic, target_relic):
#         salvage_needed, signalData_needed = calculate_mats(relic_level)
#         total_salvage_dif = [x + y for x, y in zip(total_salvage_dif, salvage_needed)]
#         total_signalData_dif = [x + y for x, y in zip(total_signalData_dif, signalData_needed)]
#
#     return total_salvage_dif, total_signalData_dif

