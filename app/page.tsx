"use client";

import React, { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from "@/components/ui/card";
import { ScrollArea, ScrollBar } from "@/components/ui/scroll-area";
import { toast } from "sonner";

interface BadgeData {
  name: string;
  markdown: string;
  markdown_code: string;
}

export default function Home() {
  const [inputText, setInputText] = useState("");
  const [generatedBadges, setGeneratedBadges] = useState<BadgeData[]>([]);
  const [invalidSlugs, setInvalidSlugs] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const generateBadges = async () => {
    const slugs = inputText.split(",").map((slug) => slug.trim());

    if (!slugs.length || slugs.every((slug) => !slug)) {
      toast.error("Please enter valid comma-separated simple-icons slugs.");
      return;
    }

    if (slugs.length > 1 && !inputText.includes(",")) {
      toast.error("Please separate slugs with commas.");
      return;
    }

    setIsLoading(true);
    setGeneratedBadges([]);
    setInvalidSlugs([]);

    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/generate_badges`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ slugs }), // Send the array of slugs
        }
      );

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(
          errorData?.error ||
            `Failed to generate badges (HTTP ${response.status})`
        );
      }

      const data = await response.json();
      setGeneratedBadges(data.badges);
      setInvalidSlugs(data.invalid_slugs);

      if (data.badges && data.badges.length > 0) {
        toast.success("Badges generated successfully!");
      } else {
        toast.error("There were no valid slugs provided.");
      }
    } catch (error: unknown) {
      console.error("Error generating badges:", error);
      if (error instanceof Error) {
        toast.error(
          error.message || "Failed to generate badges. Please try again."
        );
      } else {
        toast.error("An unknown error occurred. Please try again.");
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="min-h-screen dark:bg-black py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md mx-auto">
        <Card>
          <CardHeader>
            <CardTitle className="text-2xl font-bold text-center">
              Markdown Badge Generator
            </CardTitle>
            <CardDescription className="text-center">
              Enter comma-separated simple-icons slugs to generate badges.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="space-y-2">
                <label htmlFor="input-text" className="text-sm font-medium">
                  Simple-Icons Slugs
                </label>
                <Input
                  id="input-text"
                  placeholder="e.g., react, nextdotjs, github"
                  value={inputText}
                  onChange={(e) => setInputText(e.target.value)}
                  onKeyDown={(e) => e.key === "Enter" && generateBadges()}
                />
              </div>

              <Button
                onClick={() => {
                  generateBadges();
                }}
                className="w-full"
                disabled={isLoading}
              >
                {isLoading ? "Generating..." : "Generate Badges"}
              </Button>
            </div>
          </CardContent>
        </Card>
        {generatedBadges.length > 0 && (
          <Card className="mt-4">
            <CardHeader>
              <CardTitle className="font-bold text-center">
                Generated Badges
              </CardTitle>
              <CardDescription>
                Some badges may need the logoColor query to be set to black
                (instead of white) to match the icon, e.g., the React badge.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2">
                {generatedBadges.map((badge) => (
                  <li key={badge.name}>
                    <ScrollArea className="rounded-md border py-2 max-h-16 whitespace-nowrap overflow-auto">
                      <code>{badge.markdown}</code>
                      <ScrollBar
                        orientation="horizontal"
                        className="h-2 bg-gray-300"
                      />
                    </ScrollArea>
                  </li>
                ))}
              </ul>
            </CardContent>
          </Card>
        )}
        {invalidSlugs.length > 0 && (
          <Card className="mt-4">
            <CardHeader>
              <CardTitle className="font-bold text-center">
                Invalid Slugs
              </CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="list-disc pl-5">
                {invalidSlugs.map((slug) => (
                  <li key={slug} className="text-red-500 break-words">
                    {slug}
                  </li>
                ))}
              </ul>
            </CardContent>
          </Card>
        )}
      </div>
    </main>
  );
}
